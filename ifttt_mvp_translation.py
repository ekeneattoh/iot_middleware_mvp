from ifttt_prep import populate_ifttt_datasets, remove_special_characters, pre_processed_eupont_trigger_names, \
    pre_processed_eupont_action_names
from ifttt_translator import process_combined_similarity, process_allen_similarity, process_ifttt_rules
from os import listdir
from utils import write_to_json_file

################ DATASET PREP

# import the full dataset and record key info about it

full_recipe_list: list = populate_ifttt_datasets(filename="test_datasets/2017_05_mi_et_al_dataset/recipes.json")
mvp_recipes_to_consider: int = 30

dataset_metadata: dict = {
    "total_recipes": len(full_recipe_list),
    "total_recipes_considered": mvp_recipes_to_consider
}

write_to_json_file(filename="processed_data/mvp_results/mvp_dataset_metadata.json", data=dataset_metadata)

mvp_dataset: list = full_recipe_list[:mvp_recipes_to_consider]

# save the dataset to file
write_to_json_file(filename="processed_data/mvp_results/mvp_dataset.json", data=mvp_dataset)

# get and pre-process the triggers and actions
mvp_ifttt_test_triggers_dataset_clean = [remove_special_characters(dataset=x, dataset_key="triggerTitle") for x in
                                         mvp_dataset]

mvp_ifttt_test_actions_dataset_clean = [remove_special_characters(dataset=x, dataset_key="actionTitle") for x in
                                        mvp_dataset]

################ SPACY SIMILARITY
# compute the spacy similarity and save the results to a document
mvp_ifttt_spacy_processed_triggers = [
    process_ifttt_rules(doc1=x["triggerTitle"], word_list=pre_processed_eupont_trigger_names,
                        raw_results_subfolder_name="mvp_results/ifttt_mvp_raw_triggers/",
                        filtered_results_subfolder_name="mvp_results/ifttt_mvp_spacy_filtered_triggers/")
    for x in mvp_ifttt_test_triggers_dataset_clean]

mvp_ifttt_spacy_processed_actions = [
    process_ifttt_rules(doc1=x["actionTitle"], word_list=pre_processed_eupont_action_names,
                        raw_results_subfolder_name="mvp_results/ifttt_mvp_raw_actions/",
                        filtered_results_subfolder_name="mvp_results/ifttt_mvp_spacy_filtered_actions/")
    for x in mvp_ifttt_test_actions_dataset_clean]

################ ALENNLP SIMILARITY
# process result and save to file
mvp_ifttt_allennlp_processed_triggers = [
    process_allen_similarity(premise=x["triggerTitle"], hypothesis_list=pre_processed_eupont_trigger_names) for x in
    mvp_ifttt_test_triggers_dataset_clean]


write_to_json_file(filename="processed_data/mvp_results/ifttt_mvp_allennlp_filtered_triggers/mvp_result.json",
                   data=mvp_ifttt_allennlp_processed_triggers)

mvp_ifttt_allennlp_processed_actions = [
    process_allen_similarity(premise=x["actionTitle"], hypothesis_list=pre_processed_eupont_trigger_names) for x in
    mvp_ifttt_test_actions_dataset_clean]

write_to_json_file(filename="processed_data/mvp_results/ifttt_mvp_allennlp_filtered_actions/mvp_result.json",
                   data=mvp_ifttt_allennlp_processed_actions)

################ COMBINED SIMILARITY
TRIGGERS_INPUT_PATH = "processed_data/mvp_results/ifttt_mvp_spacy_filtered_triggers/"
ACTIONS_INPUT_PATH = "processed_data/mvp_results/ifttt_mvp_spacy_filtered_actions/"

TRIGGERS_RESULT_PATH = "processed_data/mvp_results/mvp_combined_similarity/triggers/"
ACTIONS_RESULT_PATH = "processed_data/mvp_results/mvp_combined_similarity/actions/"

triggers_filenames = listdir("processed_data/mvp_results/ifttt_mvp_spacy_filtered_triggers/")
actions_filenames = listdir("processed_data/mvp_results/ifttt_mvp_spacy_filtered_actions/")

# process the combined similarities for the triggers and actions and store the results in a file
for filename in triggers_filenames:
    if filename != ".DS_Store":
        print("Processing " + filename)
        process_combined_similarity(input_filename=TRIGGERS_INPUT_PATH + filename,
                                    result_filename=TRIGGERS_RESULT_PATH + filename)

for filename in actions_filenames:
    if filename != ".DS_Store":
        print("Processing " + filename)
        process_combined_similarity(input_filename=ACTIONS_INPUT_PATH + filename,
                                    result_filename=ACTIONS_RESULT_PATH + filename)
