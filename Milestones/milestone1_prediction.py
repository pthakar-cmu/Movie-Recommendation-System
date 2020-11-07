
from random import sample
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

movie_list = read_json('movie_set.json')
prediction_data = read_json('final_prediction.json')

def recommend(test_user, movie_list, prediction_data):
  result = []
  if test_user in prediction_data:
    result = prediction_data[test_user]
  else:
    result = sample(movie_list,20)
  return ",".join(result)

if __name__ == "__main__":
  test_user = str(sys.argv[1])
  recommend(test_user, movie_list, prediction_data)