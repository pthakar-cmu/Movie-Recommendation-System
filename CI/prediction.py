# predict the movie list

from random import randint,sample
import pandas as pd
import json
import sys
from collections import defaultdict


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

def recommend(test_user):
    movie_list = read_json('CI/movie_set.json')
    prediction_data = read_json('CI/final_prediction.json')

    result = []
    if str(test_user) in prediction_data:
        print("find it")
        result = prediction_data[str(test_user)]
    else:
        print("random")
        result = sample(movie_list,20)
    return(",".join(result))

