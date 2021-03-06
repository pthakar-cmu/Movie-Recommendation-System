from random import randint
import pandas as pd
from surprise import Reader
from surprise import KNNWithMeans, SVD
from surprise import Dataset
from surprise.model_selection import GridSearchCV, train_test_split
import joblib
import time
import re
import csv

from model_evaluation import precision_recall_at_k, get_metrics_summary, get_top_n

start_time = time.time()

# Read in data
rating_user, rating_item, rating = [], [], []
num_file = 3

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
print('Totally unique users: ' + str(len(user_set)))
print('Totally unique movies: ' + str(len(movie_set)))

with open('movie_names.csv', 'w') as f:
    write = csv.writer(f)
    write.writerows([movie_set])

# Prepare dataset
ratings_dict = {
    "item": rating_item,
    "user": rating_user,
    "rating": rating
}

df = pd.DataFrame(ratings_dict)
train_df = df.sample(frac=0.8, random_state=0)
test_df = df.drop(train_df.index)

reader = Reader(rating_scale=(1, 5))
train_data = Dataset.load_from_df(train_df[["user", "item", "rating"]], reader)
test_data = Dataset.load_from_df(test_df[["user", "item", "rating"]], reader)


# Train models using Grid Search CV
print('Start parameter search')
param_grid = {'n_epochs': [5, 10], 'lr_all': [0.002, 0.005],
              'reg_all': [0.4, 0.6]}
gs = GridSearchCV(SVD, param_grid, measures=["rmse"], cv=5)
gs.fit(train_data)
print("Best score: ", gs.best_score['rmse'])
best_params = gs.best_params["rmse"]


# Model evaluation
print('Start model evaluation')
trainset = train_data.build_full_trainset()
testset = test_data.build_full_trainset().build_testset()
algo = SVD(n_epochs=best_params['n_epochs'],
               lr_all=best_params['lr_all'],
               reg_all=best_params['reg_all'])
algo.fit(trainset)
val_predictions = algo.test(testset)
metrics = precision_recall_at_k(val_predictions)
get_metrics_summary(metrics, 'user_info.csv', 'offline_metrics_report_svd.txt', 'precision')


# Recommendation lists
print('Get recommendations')
full_data = Dataset.load_from_df(df[["user", "item", "rating"]], reader)
known_data = full_data.build_full_trainset()
predict_data = known_data.build_anti_testset()
all_predictions = algo.test(predict_data)
recommendations = get_top_n(all_predictions, 20)
rec_df = pd.DataFrame(recommendations).transpose()
rec_df.to_csv('Prediction_data.csv')

print('Done!')
