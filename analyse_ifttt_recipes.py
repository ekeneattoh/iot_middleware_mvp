from ifttt_prep import populate_ifttt_datasets
from utils import write_to_json_file

# import the full dataset and record key info about it

full_recipe_list: list = populate_ifttt_datasets(filename="test_datasets/2017_05_mi_et_al_dataset/recipes.json")

ifttt_analysis: dict = {
    "triggers": {},
    "actions": {}
}

for item in full_recipe_list:
    trigger_title = item["triggerTitle"]
    action_title = item["actionTitle"]

    print("Processing " + trigger_title)
    print("Processing " + action_title)

    if trigger_title in ifttt_analysis["triggers"].keys():
        ifttt_analysis["triggers"][trigger_title] = ifttt_analysis["triggers"][trigger_title] + 1
    else:
        ifttt_analysis["triggers"][trigger_title] = 1

    if action_title in ifttt_analysis["actions"].keys():
        ifttt_analysis["actions"][action_title] = ifttt_analysis["actions"][action_title] + 1
    else:
        ifttt_analysis["actions"][action_title] = 1

# get some general facts about the analysed data
unique_triggers = 0
duplicate_triggers = 0

unique_actions = 0
duplicate_actions = 0

for key in ifttt_analysis["triggers"].keys():
    if ifttt_analysis["triggers"][key] == 1:
        unique_triggers += 1
    elif ifttt_analysis["triggers"][key] > 1:
        duplicate_triggers += 1

for key in ifttt_analysis["actions"].keys():
    if ifttt_analysis["actions"][key] == 1:
        unique_actions += 1
    elif ifttt_analysis["actions"][key] > 1:
        duplicate_actions += 1

ifttt_analysis["summary"] = {
    "triggers_summary": {
        "unique_triggers": unique_triggers,
        "duplicate_triggers": duplicate_triggers,
        "total_triggers": len(ifttt_analysis["triggers"].keys())
    },
    "actions_summary": {
        "unique_actions": unique_actions,
        "duplicate_actions": duplicate_actions,
        "total_actions": len(ifttt_analysis["actions"].keys())
    }
}

write_to_json_file(filename="processed_data/mvp_results2/ifttt_analysis.json", data=ifttt_analysis)
