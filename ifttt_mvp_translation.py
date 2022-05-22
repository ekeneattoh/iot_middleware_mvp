from ifttt_prep import populate_ifttt_datasets, remove_special_characters, process_ifttt_rules, \
    pre_processed_eupont_trigger_names, pre_processed_eupont_action_names
from ifttt_translator import process_combined_similarity
from os import listdir
from utils import write_to_json_file

# prep the dataset

# import the full dataset and record key info about it

full_recipe_list: list = populate_ifttt_datasets(filename="test_datasets/2017_05_mi_et_al_dataset/recipes.json")
mvp_recipes_to_consider: int = 100

dataset_metadata: dict = {
    "total_recipes": len(full_recipe_list),
    "total_recipes_considered": mvp_recipes_to_consider
}

write_to_json_file(filename="processed_data/mvp_dataset_metadata.json", data=dataset_metadata)

mvp_dataset: list = full_recipe_list[:mvp_recipes_to_consider]

# save the dataset to file
write_to_json_file(filename="processed_data/mvp_dataset.json", data=mvp_dataset)

# get and pre-process the triggers and actions
mvp_ifttt_test_triggers_dataset_clean = [remove_special_characters(dataset=x, dataset_key="triggerTitle") for x in
                                         mvp_dataset]

mvp_ifttt_test_actions_dataset_clean = [remove_special_characters(dataset=x, dataset_key="actionTitle") for x in
                                        mvp_dataset]

# compute the spacy similarity and save the results to a document

mvp_ifttt_processed_triggers = [
    process_ifttt_rules(doc1=x["triggerTitle"], word_list=pre_processed_eupont_trigger_names,
                        raw_results_subfolder_name="ifttt_mvp_raw_triggers/",
                        filtered_results_subfolder_name="ifttt_mvp_flitered_triggers/")
    for x in mvp_ifttt_test_triggers_dataset_clean]

mvp_ifttt_processed_actions = [
    process_ifttt_rules(doc1=x["actionTitle"], word_list=pre_processed_eupont_action_names,
                        raw_results_subfolder_name="ifttt_mvp_raw_actions/",
                        filtered_results_subfolder_name="ifttt_mvp_filtered_actions/")
    for x in mvp_ifttt_test_actions_dataset_clean]

# compute the AllenNLP similarity
TRIGGERS_INPUT_PATH = "processed_data/ifttt_mvp_flitered_triggers/"
ACTIONS_INPUT_PATH = "processed_data/ifttt_mvp_filtered_actions/"

TRIGGERS_RESULT_PATH = "processed_data/mvp_combined_similarity/triggers/"
ACTIONS_RESULT_PATH = "processed_data/mvp_combined_similarity/actions/"

# process the triggers and actions and store the results in a file
triggers_filenames = listdir("processed_data/ifttt_mvp_flitered_triggers/")
actions_filenames = listdir("processed_data/ifttt_mvp_filtered_actions/")

for filename in triggers_filenames:
    print("Processing " + filename)
    process_combined_similarity(input_filename=TRIGGERS_INPUT_PATH + filename,
                                result_filename=TRIGGERS_RESULT_PATH + filename)

for filename in actions_filenames:
    print("Processing " + filename)
    process_combined_similarity(input_filename=ACTIONS_INPUT_PATH + filename,
                                result_filename=ACTIONS_RESULT_PATH + filename)
