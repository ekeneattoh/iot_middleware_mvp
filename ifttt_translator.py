from utils import write_to_json_file, compute_combined_similarity, sort_dict_by_value, compute_allennlp_similarity, \
    compute_spacy_word_similarity, filter_spacy_result
import json
from os import path


def sort_by_key(unsorted_list: list, key="combined_similarity"):
    # return in ascending order
    return list(reversed(sort_dict_by_value(unsorted_list=unsorted_list,
                                            sort_key=key)))


def process_allen_similarity(premise: str, hypothesis_list: list):
    result = []

    for word in hypothesis_list:
        allennlp_result = compute_allennlp_similarity(premise=premise, hypothesis=word)
        similarity_dict = {
            "ifttt_name": premise,
            "eupont_hypothesis": word,
            "allen_nlp_entailment": allennlp_result["entailment"] * 100,
            "allen_nlp_contradiction": allennlp_result["contradiction"] * 100,
            "allen_nlp_neutral": allennlp_result["neutral"] * 100
        }
        print("adding result for " + word)
        result.append(similarity_dict)

    return sort_by_key(unsorted_list=result, key="allen_nlp_entailment")


def process_combined_similarity(input_filename: str, result_filename: str):
    trigger_dataset_file = open(file=input_filename)
    trigger_dataset = json.load(trigger_dataset_file)

    trigger_similarity = compute_combined_similarity(dataset=trigger_dataset)

    if path.exists(result_filename):
        print(result_filename + " already exists")
    else:
        write_to_json_file(filename=result_filename,
                           data=sort_by_key(unsorted_list=trigger_similarity))


def process_ifttt_rules(doc1: str, word_list: list, raw_results_subfolder_name: str,
                        filtered_results_subfolder_name: str):
    main_folder = "processed_data/"

    raw_data_filename = main_folder + raw_results_subfolder_name + doc1 + "_ifttt_result.json"

    filtered_data_filename = main_folder + filtered_results_subfolder_name + doc1 + "_ifttt_result.json"

    if path.exists(raw_data_filename) and path.exists(filtered_data_filename):
        print(doc1 + " files have already been created!")
    else:
        result = compute_spacy_word_similarity(doc1=doc1, word_list=word_list)

        write_to_json_file(filename=raw_data_filename, data=result)

        write_to_json_file(filename=filtered_data_filename, data=filter_spacy_result(dataset=result, threshold=55))

        print(doc1 + " files were just created!")
