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

    return sort_by_key(unsorted_list=result)


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


#####################################################################################################

if "__name__" == "__main__":
    # select popular Trigger-Action-Programming Rule use-cases and run ALLEN NLP algorithm on them
    # select 3 popular use-cases for experimentation sake

    # Temperature Event
    # IFTTT Trigger Name: High Temperature (Smart Thermostat)
    high_temperature_dataset_file = open("processed_data/filtered_triggers/High temperature_ifttt_result.json")
    high_temperature_dataset = json.load(high_temperature_dataset_file)

    high_temperature_combined_similarity = compute_combined_similarity(dataset=high_temperature_dataset)

    write_to_json_file(filename="processed_data/combined_similarity/high_temperature_combined.json",
                       data=sort_by_key(unsorted_list=high_temperature_combined_similarity))

    # Motion Event
    # IFTTT Trigger Name: Motion detected (Motion Sensor)
    motion_detected_dataset_file = open("processed_data/filtered_triggers/Motion detected_ifttt_result.json")
    motion_detected_dataset = json.load(motion_detected_dataset_file)

    motion_detected_combined_similarity = compute_combined_similarity(dataset=motion_detected_dataset)

    write_to_json_file(filename="processed_data/combined_similarity/motion_detected_combined.json",
                       data=sort_by_key(unsorted_list=motion_detected_combined_similarity))

    # Time Event
    # IFTTT Trigger Name: Your Alarm goes off (Time Trigger)
    alarm_goes_off_dataset_file = open("processed_data/filtered_triggers/Your Alarm goes off_ifttt_result.json")
    alarm_goes_off_dataset = json.load(alarm_goes_off_dataset_file)

    alarm_goes_off_combined_similarity = compute_combined_similarity(dataset=alarm_goes_off_dataset)

    write_to_json_file(filename="processed_data/combined_similarity/alarm_goes_off_combined.json",
                       data=sort_by_key(unsorted_list=alarm_goes_off_combined_similarity))

    #############################################################################################
    # pick some Actions for testing purposes

    # set temperature
    set_temperature_dataset_file = open("processed_data/filtered_actions/Set temperature_ifttt_result.json")
    set_temperature_dataset = json.load(set_temperature_dataset_file)

    set_temperature_combined_similarity = compute_combined_similarity(dataset=set_temperature_dataset)

    write_to_json_file(filename="processed_data/combined_similarity/set_temperature_action_combined.json",
                       data=sort_by_key(unsorted_list=set_temperature_combined_similarity))

    # smart lock
    disarm_security_system_dataset_file = open("processed_data/filtered_actions/Disarm system_ifttt_result.json")
    disarm_security_system_dataset = json.load(disarm_security_system_dataset_file)

    disarm_security_system_combined_similarity = compute_combined_similarity(dataset=disarm_security_system_dataset)

    write_to_json_file(filename="processed_data/combined_similarity/disarm_security_system_combined.json",
                       data=sort_by_key(unsorted_list=disarm_security_system_combined_similarity))

    # smart switch
    turn_on_switch_dataset_file = open("processed_data/filtered_actions/Turn on switch_ifttt_result.json")
    turn_on_switch_dataset = json.load(turn_on_switch_dataset_file)

    turn_on_switch_combined_similarity = compute_combined_similarity(dataset=turn_on_switch_dataset)

    write_to_json_file(filename="processed_data/combined_similarity/turn_on_switch_combined.json",
                       data=sort_by_key(unsorted_list=turn_on_switch_combined_similarity))
