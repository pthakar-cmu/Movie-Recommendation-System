# This is dummy ml pipeline file for testing

from data import get_data
from preprocessing import preprocess_data
from training import train_model
from evaluation import evaluate_model_offline

# fetch fata from Kafka stream
data_dict = get_data()

# Preprocessing the data 
train_df, test_df, df = preprocess_data(data_dict)

# train model
model = train_model(train_df, test_df)

# evaluate the model offline
evaluate_model_offline(model, df)
