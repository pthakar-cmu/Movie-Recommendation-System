import pytest 
import pandas as pd
import re

import os
import sys

root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from data import get_data

def test_data():
        rating_dict = get_data()
        rating_item= rating_dict["item"]
        rating_user = rating_dict["user"]
        rating = rating_dict["rating"]
        for i in range(len(rating)):
                assert isinstance(rating_user[i], int) == True   
                assert isinstance(rating_item[i], str) == True
                assert isinstance(rating[i], int)  == True
                

