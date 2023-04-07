from ifttt_prep import populate_ifttt_datasets, remove_special_characters, pre_processed_eupont_trigger_names, \
    pre_processed_eupont_action_names
from ifttt_translator import process_combined_similarity, process_allen_similarity, process_ifttt_rules
from os import listdir
from utils import write_to_json_file
import json
from random import randint

################ DATASET PREP

# import the full dataset and record key info about it

# full_recipe_list: list = populate_ifttt_datasets(filename="test_datasets/2017_05_mi_et_al_dataset/recipes.json")
# mvp_recipes_to_consider: int = 100
#
# dataset_metadata: dict = {
#     "total_recipes": len(full_recipe_list),
#     "total_recipes_considered": mvp_recipes_to_consider
# }
#
# write_to_json_file(filename="processed_data/mvp_results2/mvp_dataset_metadata.json", data=dataset_metadata)
#
# mvp_dataset: list = full_recipe_list[:mvp_recipes_to_consider]

mvp_cluster_file = open("processed_data/" + RESULTS_FOLDER + "/ifttt_analysis.json") # consider only entries uses 1000 and above times
# 44 triggers
# 45 actions

mvp_cluster_data = json.load(mvp_cluster_file)

RESULTS_FOLDER = "mvp_results3"

random_start_zero = randint(0, 100)

# first dataset
mvp_cluster_triggers: list = mvp_cluster_data["triggers"].keys()

mvp_cluster_actions: list = mvp_cluster_data["actions"].keys()

# second dataset
mvp_cluster_triggers_one: list = mvp_cluster_data["triggers"].keys()

mvp_cluster_actions_one: list = mvp_cluster_data["actions"].keys()

# save the dataset to file
# write_to_json_file(filename="processed_data/mvp_results2/mvp_dataset.json", data=mvp_dataset)

################ SPACY SIMILARITY
# compute the spacy similarity and save the results to a document
mvp_ifttt_spacy_processed_triggers = [
    process_ifttt_rules(doc1=x, word_list=pre_processed_eupont_trigger_names,
                        raw_results_subfolder_name=RESULTS_FOLDER + "/ifttt_mvp_raw_triggers/",
                        filtered_results_subfolder_name=RESULTS_FOLDER + "/ifttt_mvp_spacy_filtered_triggers/")
    for x in mvp_cluster_triggers]

mvp_ifttt_spacy_processed_actions = [
    process_ifttt_rules(doc1=x, word_list=pre_processed_eupont_action_names,
                        raw_results_subfolder_name=RESULTS_FOLDER + "/ifttt_mvp_raw_actions/",
                        filtered_results_subfolder_name=RESULTS_FOLDER + "/ifttt_mvp_spacy_filtered_actions/")
    for x in mvp_cluster_actions]

################ ALENNLP SIMILARITY
# process result and save to file
mvp_ifttt_allennlp_processed_triggers = [
    process_allen_similarity(premise=x, hypothesis_list=pre_processed_eupont_trigger_names) for x in
    mvp_cluster_triggers]

write_to_json_file(
    filename="processed_data/" + RESULTS_FOLDER + "/ifttt_mvp_allennlp_filtered_triggers/mvp_result.json",
    data=mvp_ifttt_allennlp_processed_triggers)

mvp_ifttt_allennlp_processed_actions = [
    process_allen_similarity(premise=x, hypothesis_list=pre_processed_eupont_action_names) for x in
    mvp_cluster_actions]

write_to_json_file(filename="processed_data/" + RESULTS_FOLDER + "/ifttt_mvp_allennlp_filtered_actions/mvp_result.json",
                   data=mvp_ifttt_allennlp_processed_actions)

################ COMBINED SIMILARITY
TRIGGERS_INPUT_PATH = "processed_data/" + RESULTS_FOLDER + "/ifttt_mvp_spacy_filtered_triggers/"
ACTIONS_INPUT_PATH = "processed_data/" + RESULTS_FOLDER + "/ifttt_mvp_spacy_filtered_actions/"

TRIGGERS_RESULT_PATH = "processed_data/" + RESULTS_FOLDER + "/mvp_combined_similarity/triggers/"
ACTIONS_RESULT_PATH = "processed_data/" + RESULTS_FOLDER + "/mvp_combined_similarity/actions/"

triggers_filenames = listdir("processed_data/" + RESULTS_FOLDER + "/ifttt_mvp_spacy_filtered_triggers/")
actions_filenames = listdir("processed_data/" + RESULTS_FOLDER + "/ifttt_mvp_spacy_filtered_actions/")

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
