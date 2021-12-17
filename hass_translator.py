from utils import read_yaml_file, write_to_json_file
from utils import compute_spacy_word_similarity
import json
from os import path

hass_example_rules = read_yaml_file(
    filename="/Users/ekeneattoh/Documents/Portfolio_and_Personal_Documents/Personal_Development/PhD/PhD_Docs/eattoh"
             "-phd/iot_middleware_mvp/home_assistant_test/config/automations.yaml")

print(hass_example_rules)

hass_triggers = ["time", "geo location"]

eupont_data_file = open("eupont_processed.json")

eupont_data = json.load(eupont_data_file)

pre_processed_eupont_trigger_names = eupont_data["eupont_triggers"]

for trigger in hass_triggers:
    result = compute_spacy_word_similarity(doc1=trigger, word_list=pre_processed_eupont_trigger_names)

    filename = "processed_data/" + trigger + "_hass_result.json"

    # write the result to a json file
    write_to_json_file(filename=filename, data=result)

    if path.exists(filename):
        print(filename + " has been created!")
    else:
        print(filename + " was not created!")

# get the trigger's platform and try and find which trigger from EUPont it matches.
