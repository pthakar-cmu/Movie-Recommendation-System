from random import randint
import pandas as pd
from surprise import Reader
from surprise import KNNWithMeans
from surprise import Dataset
import joblib
import time
import re
import csv

start_time = time.time()

rating_user, rating_item, rating = [], [], []
num_file = 474

for ind_file in range(num_file):
  rating_file_name = "part-"
  for ind_zero in range(5 - len(str(ind_file))):
    rating_file_name += "0"
  rating_file_name += str(ind_file)
  rating_file = open('KafkaData/userRating/' + rating_file_name, "r")
  rating_file_content = rating_file.readlines()
  for ind_line in range(len(rating_file_content)):
    seg = re.findall(r"'[ a-zA-Z._\-+*0-9]+'", rating_file_content[ind_line])

    try:
      rating.append(int(seg[2][1:-1]))
    except:
      continue

    try:
        rating_user.append(int(seg[0][1:-1]))
    except:
        rating.pop()
        continue
    rating_item.append(seg[1][1:-1])

  rating_file.close()

user_set = list(set(rating_user))
movie_set = list(set(rating_item))

with open('movie_names.csv', 'w') as f:
    write = csv.writer(f)
    write.writerows([movie_set])

ratings_dict = {
    "item": rating_item,
    "user": rating_user,
    "rating": rating
}

df = pd.DataFrame(ratings_dict)
reader = Reader(rating_scale=(1, 5))
data = Dataset.load_from_df(df[["user", "item", "rating"]], reader)
sim_options = {                       # To use user-based cosine similarity
    "name": "cosine",
    "user_based": True,
}
algo = KNNWithMeans(sim_options=sim_options)

trainingSet = data.build_full_trainset()
algo.fit(trainingSet)

final_prediction = {}
for i in range(len(user_set)):
  predict_dict = {}
  for ind in range(len(movie_set)):
    prediction = algo.predict(user_set[i], movie_set[ind])
    predict_dict[prediction.est] = movie_set[ind]
  ind = 1
  result = []
  for score in sorted(predict_dict, reverse=True):
    result.append(predict_dict[score])
    ind += 1
    if ind > 20:
      final_prediction[user_set[i]] = result
      break

with open('Prediction_data.csv', 'w') as f:
    for key in final_prediction.keys():
        f.write("%s, %s\n" % (key, final_prediction[key]))