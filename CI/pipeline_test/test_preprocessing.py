import pytest 
import pandas as pd
import re
from preprocessing import preprocess_data

def test_preprocessing():
        data_dict = {
                "item": ['a','b','c','d','e'],
                "user": [1,2,3,4,5],
                "rating": [5,4,3,2,1]
        }
        train_df, test_df, df = preprocess_data(data_dict)
        assert len(train_df) == 4
        assert len(test_df) == 1
        assert len(df) == 5


                

