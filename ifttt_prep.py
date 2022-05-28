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