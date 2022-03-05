from utils import write_to_json_file, compute_combined_similarity, sort_dict_by_value
import json
from os import path


def sort_by_allen_entailment(unsorted_list: list):
    # return in ascending order
    return list(reversed(sort_dict_by_value(unsorted_list=unsorted_list,
                                            sort_key="allen_nlp_entailment")))


#####################################################################################################

# select popular Trigger-Action-Programming Rule use-cases and run ALLEN NLP algorithm on them
# select 3 popular use-cases for experimentation sake

# Temperature Event
# IFTTT Trigger Name: High Temperature
high_temperature_dataset_file = open("processed_data/filtered_triggers/High temperature_ifttt_result.json")
high_temperature_dataset = json.load(high_temperature_dataset_file)

high_temperature_combined_similarity = compute_combined_similarity(dataset=high_temperature_dataset)

write_to_json_file(filename="processed_data/combined_similarity/high_temperature_combined.json",
                   data=sort_by_allen_entailment(unsorted_list=high_temperature_combined_similarity))

# Motion Event
# IFTTT Trigger Name: Motion detected
motion_detected_dataset_file = open("processed_data/filtered_triggers/Motion detected_ifttt_result.json")
motion_detected_dataset = json.load(motion_detected_dataset_file)

motion_detected_combined_similarity = compute_combined_similarity(dataset=motion_detected_dataset)

write_to_json_file(filename="processed_data/combined_similarity/motion_detected_combined.json",
                   data=sort_by_allen_entailment(unsorted_list=motion_detected_combined_similarity))

# Time Event
# IFTTT Trigger Name: Your Alarm goes off
alarm_goes_off_dataset_file = open("processed_data/filtered_triggers/Your Alarm goes off_ifttt_result.json")
alarm_goes_off_dataset = json.load(alarm_goes_off_dataset_file)

alarm_goes_off_combined_similarity = compute_combined_similarity(dataset=alarm_goes_off_dataset)

write_to_json_file(filename="processed_data/combined_similarity/alarm_goes_off_combined.json",
                   data=sort_by_allen_entailment(unsorted_list=alarm_goes_off_combined_similarity))



#############################################################################################
# pick one Action for testing purposes

turn_on_ac_unit_dataset_file = open("processed_data/filtered_actions/Turn AC unit on_ifttt_result.json")
turn_on_ac_unit_dataset = json.load(turn_on_ac_unit_dataset_file)

turn_on_ac_unit_combined_similarity = compute_combined_similarity(dataset=turn_on_ac_unit_dataset)

write_to_json_file(filename="processed_data/combined_similarity/turn_on_ac_unit_action_combined.json",
                   data=sort_by_allen_entailment(unsorted_list=turn_on_ac_unit_combined_similarity))
