# This is dummy ml pipeline file for testing

from data import get_data
from preprocessing import preprocess_data
from training import train_model
from evaluation import evaluate_model_offline


# Fetch data from Kafka stream
num_file = get_data()

# Preprocessing the data
rating_user, rating_item, rating, user_set, movie_set = preprocess_data(num_file)

# train model
train_model(rating_user, rating_item, rating, user_set, movie_set)

# evaluate the model offline
evaluate_model_offline(12345)
evaluate_model_offline(11880)