# data preprocessing

import pandas as pd
import re
import json

def preprocess_data(ratings_dict):

    # split dataset into traiing data and test data
    df = pd.DataFrame(ratings_dict)
    train_df = df.sample(frac=0.8, random_state=0)
    test_df = df.drop(train_df.index)
    
        
    return [train_df, test_df, df]