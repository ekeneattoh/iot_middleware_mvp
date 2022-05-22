from utils import compute_spacy_word_similarity, write_to_json_file, filter_spacy_result
import json
from os import path

eupont_data_file = open("eupont_processed.json")
eupont_data = json.load(eupont_data_file)

pre_processed_eupont_trigger_names: list = eupont_data["eupont_triggers"]

pre_processed_eupont_action_names: list = eupont_data["eupont_actions"]


def populate_ifttt_datasets(filename: str) -> list:
    dataset_list: list = []
    with open(filename, 'r') as f:
        for line in f:
            dataset_list.append(json.loads(line))

    return dataset_list


def process_ifttt_rules(doc1: str, word_list: list, raw_results_subfolder_name: str,
                        filtered_results_subfolder_name: str):
    result = compute_spacy_word_similarity(doc1=doc1, word_list=word_list)

    main_folder = "processed_data/"

    raw_data_filename = main_folder + raw_results_subfolder_name + doc1 + "_ifttt_result.json"

    filtered_data_filename = main_folder + filtered_results_subfolder_name + doc1 + "_ifttt_result.json"

    # write the result to a json file
    if path.exists(raw_data_filename) or path.exists(filtered_data_filename):
        print(raw_data_filename + " has already  been created!")
    else:
        # write the raw processed_data to file
        write_to_json_file(filename=raw_data_filename, data=result)
        print(raw_data_filename + " was just created!")

        # write the filtered processed data to file, i.e remove data with similarity below a threshold
        write_to_json_file(filename=filtered_data_filename, data=filter_spacy_result(dataset=result, threshold=55))
        print(filtered_data_filename + " was just created!")


def remove_special_characters(dataset: dict, dataset_key: str):
    if "/" in dataset[dataset_key]:
        dataset[dataset_key] = dataset[dataset_key].replace("/", "")

    return dataset


#####################################################################################################

# do some basic pre-processing and run spacy similarity on the datasets

if "__name__" == "__main__":

    ifttt_test_triggers_dataset: list = populate_ifttt_datasets(filename="test_datasets/triggerList.json")

    ifttt_test_actions_dataset = populate_ifttt_datasets(filename="test_datasets/actionList.json")

    print("IFTTT TEST DATASET TRIGGERS: " + str(len(ifttt_test_triggers_dataset)))

    ifttt_test_triggers_dataset_clean = [remove_special_characters(dataset=x, dataset_key="triggerTitle") for x in
                                         ifttt_test_triggers_dataset]

    ifttt_processed_triggers = [
        process_ifttt_rules(doc1=x["triggerTitle"], word_list=pre_processed_eupont_trigger_names,
                            raw_results_subfolder_name="raw_triggers/",
                            filtered_results_subfolder_name="filtered_triggers/")
        for x in ifttt_test_triggers_dataset_clean[:100]]

    print("IFTTT TEST DATASET ACTIONS: " + str(len(ifttt_test_actions_dataset)))

    ifttt_test_actions_dataset_clean = [remove_special_characters(dataset=x, dataset_key="actionTitle") for x in
                                        ifttt_test_actions_dataset]

    ifttt_processed_actions = [
        process_ifttt_rules(doc1=x["actionTitle"], word_list=pre_processed_eupont_action_names,
                            raw_results_subfolder_name="raw_actions/", filtered_results_subfolder_name="filtered_actions/")
        for x in ifttt_test_actions_dataset_clean[:100]]

