import pytest 
import pandas as pd
import re

import os
import sys

root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from training import train_model
import pandas as pd

def test_training():
        train_dict = {
                "item": ['a','b','c','d','a','b','c','d'],
                "user": [1,2,3,4,1,2,3,4],
                "rating": [5,4,3,2,5,4,3,2]
        }
        test_dict = {
                "item": ['e','e'],
                "user": [5,5],
                "rating": [1,1]
        }
        data_dict = {
                "item": ['a','b','c','d','e','a','b','c','d','e'],
                "user": [1,2,3,4,5,1,2,3,4,5],
                "rating": [5,4,3,2,1,5,4,3,2,1]
        }
        train_df = pd.DataFrame(train_dict)
        test_df = pd.DataFrame(test_dict)
        df = pd.DataFrame(data_dict)
        model = train_model(train_df, test_df)
        predict = model.predict(1,'e')
        assert predict.est <= 5
        assert predict.est >= 1



                

