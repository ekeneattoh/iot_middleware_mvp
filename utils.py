import yaml
import regex as re
import spacy
import json
from allennlp.predictors.predictor import Predictor

allen_nlp_predictor = Predictor.from_path("decomposable-attention-elmo-2020.04.09.tar.gz")


def read_yaml_file(filename: str) -> list:
    """

    :param filename: yaml file you want to parse
    :return: list
    """

    with open(filename, "r") as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)


def split_joined_words(joined_words_list: list):
    """
    :param joined_words_list: list of joined words to be split
    :return:
    """

    return [re.sub(r"([A-Z])", r" \1", x).split() for x in joined_words_list]


def join_split_words(split_words_list: list):
    """
    :param split_words_list: list of split words
    :return:
    """
    return [" ".join(x) for x in split_words_list]


def pre_process_word(word_list: list):
    """
    :param word_list:
    :return: e.g. ['AGoodDog'] -> ['A Good Dog']
    """

    split_words = split_joined_words(joined_words_list=word_list)

    return join_split_words(split_words_list=split_words)


def compute_spacy_word_similarity(doc1: str, word_list: list) -> dict:
    nlp = spacy.load("en_core_web_lg")

    doc1 = nlp(doc1)

    result = dict()

    for trigger in word_list:
        doc2 = nlp(trigger)
        # Similarity of two documents
        result[trigger] = {
            "ifttt_trigger_name": doc1.text,
            "similarity": doc1.similarity(doc2)
        }

    # we will return the results with the highest similarity first (in descending order)
    return {k: v for k, v in sorted(result.items(), key=lambda item: item[1]["similarity"], reverse=True)}


def filter_spacy_result(dataset: dict, threshold: int) -> list:
    return [{x: dataset[x]} for x in dataset.keys() if dataset[x]["similarity"] * 100 >= threshold]


def write_to_json_file(filename: str, data: object):
    """
    :param data:
    :param filename:
    :return:
    """
    with open(filename, 'w') as f:
        json.dump(data, f)


def compute_allennlp_similarity(premise: str, hypothesis: str, predictor) -> dict:
    result = predictor.predict(
        premise=premise,
        hypothesis=hypothesis
    )

    return {
        # likelihood in % that premise entails the hypothesis
        # i.e input statement and hypothesis statement mean the same thing
        "entailment": result["label_probs"][0],
        # likelihood in % that the input statement means something different from the
        # hypothesis statement
        "contradiction": result["label_probs"][1],
        # neutrality
        "neutral": result["label_probs"][2],
    }


def compute_combined_similarity(dataset: list) -> list:
    """
    We will compute the ALLEN nlp of a dataset which has had its Spacy similarity computed already
    We will then retun the ALLEN nlp result, the Spacy similarity as well as the average of both
    similarities. The reasoning would be that items with the highest combined similarities
    and low contradiction are indeed similar.

    :param dataset: dataset containing a dictionary of hypotheses and premises
    :return: ALLEN NLP similarity dict, spacy similarity and average of both similarities
    """

    result_list = []

    for item in dataset:
        result = {}

        premise = item[list(item.keys())[0]]["ifttt_trigger_name"]
        hypothesis = list(item.keys())[0]
        spacy_similarity = (item[list(item.keys())[0]]["similarity"]) * 100

        # compute the ALLEN nlp similarity
        allen_nlp_similarity = compute_allennlp_similarity(premise=premise, hypothesis=hypothesis,
                                                           predictor=allen_nlp_predictor)

        result["ifttt_trigger_name"] = premise
        result["eupont_hypothesis"] = hypothesis
        result["spacy_similarity"] = spacy_similarity
        result["allen_nlp_entailment"] = allen_nlp_similarity["entailment"] * 100
        result["allen_nlp_contradiction"] = allen_nlp_similarity["contradiction"] * 100
        result["allen_nlp_neutral"] = allen_nlp_similarity["neutral"] * 100
        result["combined_similarity"] = (spacy_similarity + allen_nlp_similarity["entailment"] * 100) / 2

        result_list.append(result)

    return result_list
