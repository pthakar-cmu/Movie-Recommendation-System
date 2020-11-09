# train model

from random import randint
import pandas as pd
from surprise import Reader
from surprise import KNNWithMeans
from surprise import Dataset
import re
import json
from surprise.model_selection import GridSearchCV, train_test_split
from evaluation import get_metrics_summary, get_top_n, precision_recall_at_k

def train_model(rating_user, rating_item, rating, user_set, movie_set):
    ratings_dict = {
        "item": rating_item,
        "user": rating_user,
        "rating": rating
    }

    # split dataset into traiing data and test data
    df = pd.DataFrame(ratings_dict)
    train_df = df.sample(frac=0.8, random_state=0)
    test_df = df.drop(train_df.index)

    reader = Reader(rating_scale=(1, 5))
    train_data = Dataset.load_from_df(train_df[["user", "item", "rating"]], reader)
    test_data = Dataset.load_from_df(test_df[["user", "item", "rating"]], reader)

    # Train models using Grid Search CV
    print('Start parameter search')
    param_grid = {'k': [30, 40, 50]}
    gs = GridSearchCV(KNNWithMeans, param_grid, measures=["rmse"], cv=5)
    gs.fit(train_data)
    print("Best score: ", gs.best_score['rmse'])
    best_params = gs.best_params["rmse"]

    # Model evaluation
    print('Start model evaluation')
    trainset = train_data.build_full_trainset()
    testset = test_data.build_full_trainset().build_testset()
    sim_options = {"name": "cosine", "user_based": True}
    algo = KNNWithMeans(k=best_params['k'], sim_options=sim_options)
    algo.fit(trainset)
    val_predictions = algo.test(testset)
    metrics = precision_recall_at_k(val_predictions)
    get_metrics_summary(metrics, 'CI/user_info.csv', 'CI/offline_metrics_report_knn.txt', 'precision')

    # Recommendation lists
    print('Get recommendations')
    full_data = Dataset.load_from_df(df[["user", "item", "rating"]], reader)
    known_data = full_data.build_full_trainset()
    predict_data = known_data.build_anti_testset()
    all_predictions = algo.test(predict_data)
    recommendations = get_top_n(all_predictions, 20)

    with open('CI/final_prediction.json', "w") as outfile:  
        json.dump(recommendations, outfile) 