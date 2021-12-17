import json
from utils import pre_process_word, write_to_json_file

filename = "eupont_processed.json"

eupont_json_file = open("eupont.json")
eupont_json: json = json.load(eupont_json_file)

eupont_classes = eupont_json["RDF"]["Class"]

eupont_triggers: list = [x["label"] for x in eupont_classes if x["label"].find("Trigger") != -1]
eupont_actions: list = [x["label"] for x in eupont_classes if x["label"].find("Action") != -1]

# remove the suffix word Trigger and Action from the triggers and actions including the base classes Trigger and Action
eupont_trigger_names: list = [x.removesuffix("Trigger") for x in eupont_triggers]
eupont_action_names: list = [x.removesuffix("Action") for x in eupont_actions]

print("trigger names:")
# split the joined words and turn into a single String in order to use in the NLP step
# this is because the words don't have any word vector while they are conjoined
# https://stackoverflow.com/questions/55921104/spacy-similarity-warning-evaluating-doc-similarity-based-on-empty-vectors

pre_processed_eupont_trigger_names = pre_process_word(word_list=eupont_trigger_names)
print(pre_processed_eupont_trigger_names)

print("action names:")
pre_processed_eupont_action_names = pre_process_word(word_list=eupont_action_names)
print(pre_processed_eupont_action_names)

result = {
    "eupont_triggers": pre_processed_eupont_trigger_names,
    "eupont_actions": pre_processed_eupont_action_names
}

write_to_json_file(filename=filename, data=result)
