import os
import sys

root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from evaluation import evaluate_model_offline
import pandas as pd
from surprise import Dataset
from surprise import Reader
from surprise import KNNWithMeans

def test_prediction():
        ratings_dict = {
                "item": ['a','b','c','d','e','a','b','c','d','e','a','b','c','d','e','a','b','c','d','e','a','b','c','d','e','a','b','c','d','e','a','b','c','d','e','a','b','c','d','e'],
                "user": [1,2,3,4,5,1,2,3,4,5,1,2,3,4,5,1,2,3,4,5,1,2,3,4,5,1,2,3,4,5,1,2,3,4,5,1,2,3,4,5],
                "rating": [5,4,3,2,1,5,4,3,2,1,5,4,3,2,1,5,4,3,2,1,5,4,3,2,1,5,4,3,2,1,5,4,3,2,1,5,4,3,2,1]
        }

        df = pd.DataFrame(ratings_dict)
        reader = Reader(rating_scale=(1, 5))

        data = Dataset.load_from_df(df[["user", "item", "rating"]], reader)

        sim_options = {
        "name": "cosine",
        "user_based": True,
        }
        algo = KNNWithMeans(sim_options=sim_options)
        trainset = data.build_full_trainset()
        testset = data.build_full_trainset().build_testset()
        algo.fit(trainset)
        algo.test(testset)
        result = evaluate_model_offline(algo, df)

        assert len(result) == 5




                

