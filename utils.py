import yaml
import regex as re
import spacy
import json
from allennlp.predictors.predictor import Predictor


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


def compute_allennlp_similarity(premise: str, hypothesis: str) -> dict:
    predictor = Predictor.from_path("decomposable-attention-elmo-2020.04.09.tar.gz")
    result = predictor.predict(
        premise=premise,
        hypothesis=hypothesis
    )

    return {
        "entailment": result["label_probs"][0],
        "contradiction": result["label_probs"][1],
        "neutral": result["label_probs"][2],
    }
