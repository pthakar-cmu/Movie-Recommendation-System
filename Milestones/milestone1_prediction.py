# from random import randint
# import pandas as pd
# from surprise import Reader
# from surprise import KNNWithMeans
# from surprise import Dataset
from datetime import datetime
from random import sample
import joblib
import time
# import re
import csv
import sys
import time



#print("--- %s seconds ---" % (time.time() - start_time))

#test_user = int(sys.argv[1])
#test_user = "997661"
#test_user = rating_user[randint(0,len(rating_user))]
#print("test user:", test_user)



result = []

def readFile():
  return result

def recommend(test_user):
  result = []
  start_time = time.time()
  filename = 'finalized_model.sav'
  algo = joblib.load(filename)

  start = int(round(time.time() * 1000))
  with open('training_data.csv', newline='') as f:
    reader = csv.reader(f)
    lists = list(reader)
    rating_user = lists[0]
    rating_item = lists[1]

  if str(test_user) in rating_user:

    predict_dict = {}

    for ind in range(len(rating_item)):
      prediction = algo.predict(test_user, rating_item[ind])
      predict_dict[prediction.est] = rating_item[ind]

    ind = 1
    for score in sorted(predict_dict, reverse=True):
      #print("top #", ind)
      #print("score:", score)
      #print("movie id:" + predict_dict[score])
      result.append(predict_dict[score])
      ind += 1
      if ind > 20:
        break
  else:
      result = sample(rating_item,20)

  print("-> ",int(round(time.time() * 1000))-start)
  return ",".join(result)

if __name__ == "__main__":
  test_user = int(sys.argv[1])
  recommend(test_user)

#print("--- %s seconds ---" % (time.time() - start_time))w