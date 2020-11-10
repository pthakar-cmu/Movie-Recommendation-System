import pytest 
import pandas as pd
import re
import path
import sys

folder = path.path(__file__).abspath()
sys.path.append(folder.parent.parent)


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
                

