# train model

from random import randint
import pandas as pd
from surprise import Reader
from surprise import KNNWithMeans
from surprise import Dataset
import re
import json

def train_model(rating_user, rating_item, rating, user_set, movie_set):
    ratings_dict = {
        "item": rating_item,
        "user": rating_user,
        "rating": rating
    }

    df = pd.DataFrame(ratings_dict)
    reader = Reader(rating_scale=(1, 5))
    data = Dataset.load_from_df(df[["user", "item", "rating"]], reader)
    sim_options = {                       
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

    with open('CI/final_prediction.json', "w") as outfile:  
        json.dump(final_prediction, outfile) 