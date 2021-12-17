from utils import write_to_json_file, compute_allennlp_similarity
import json
from os import path

#####################################################################################################
# try using AllenNLP on the results after using spacy similarity, to look for at the contradiction scores
test_files = ["High humidity_ifttt_result.json", "Motion detected_ifttt_result.json",
              "Temperature drops below a threshold_ifttt_result.json", "Your Alarm goes off_ifttt_result.json"]


# print(compute_allennlp_similarity(premise="Air Quality is unhealthy", hypothesis="Decreased Air Pressure"))

#####################################################################################################
# use AllenNLP first then use spacy similarity
