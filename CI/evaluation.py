# evaluate the model offline

from random import randint,sample
import pandas as pd
import json
import sys

def validate(test_user):
  try:
    int(test_user)
    return True
  except:
    return False

def read_json(name):
  with open(name) as f:
    data = json.load(f)
  return data

def evaluate_model_offline(test_user):
    movie_list = read_json('CI/movie_set.json')
    prediction_data = read_json('CI/final_prediction.json')

    result = []
    if test_user in prediction_data:
        result = prediction_data[test_user]
    else:
        result = sample(movie_list,20)
    print(",".join(result))