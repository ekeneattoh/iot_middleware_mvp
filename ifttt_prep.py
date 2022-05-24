import json

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
                            raw_results_subfolder_name="raw_actions/",
                            filtered_results_subfolder_name="filtered_actions/")
        for x in ifttt_test_actions_dataset_clean[:100]]
