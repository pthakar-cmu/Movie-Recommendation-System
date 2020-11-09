# This is dummy ml pipeline file for testing

from preprocessing import preprocess_data
from training import train_model
from evaluation import evaluate_model_offline


# Preprocessing the data retched from Kafka stream
train_df, test_df, df = preprocess_data(2)

# train model
train_model(train_df, test_df, df)

# evaluate the model offline
evaluate_model_offline(12345)
evaluate_model_offline(11880)