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

rating_user = []
rating_item = []
rating = []

num_file = 5

for ind_file in range(num_file):
  rating_file_name = "part-"
  for ind_zero in range(5 - len(str(ind_file))):
    rating_file_name += "0"
  rating_file_name += str(ind_file)
  #print("rating file name:" + rating_file_name)
  rating_file = open('KafkaData/userRating/' + rating_file_name, "r")
  rating_file_content = rating_file.readlines()
  #print("num of lines of rating:" , len(rating_file_content))
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


#print("num of user on rating:" , len(rating_user))
#print("num of item on rating:" , len(rating_item))
#print("num of rating:" , len(rating))


with open('training_data.csv', 'w') as f:
    # using csv.writer method from CSV package
    write = csv.writer(f)
    write.writerows([rating_user,rating_item])

#print("--- %s seconds ---" % (time.time() - start_time))

ratings_dict = {
    "item": rating_item,
    "user": rating_user,
    "rating": rating
}


df = pd.DataFrame(ratings_dict)
reader = Reader(rating_scale=(1, 5))

# Loads Pandas dataframe3
data = Dataset.load_from_df(df[["user", "item", "rating"]], reader)

# To use user-based cosine similarity
sim_options = {
    "name": "cosine",
    "user_based": True,
}
algo = KNNWithMeans(sim_options=sim_options)

# Train
trainingSet = data.build_full_trainset()
algo.fit(trainingSet)


filename = 'finalized_model.sav'
joblib.dump(algo, filename)

#print("--- %s seconds ---" % (time.time() - start_time))



