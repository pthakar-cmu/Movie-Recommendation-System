import pytest 
import pandas as pd
import re

def test_data():
        rating_user, rating_item, rating = data()
        for i in range(len(rating)):
                assert isinstance(rating_user[i], int) == True
                assert isinstance(rating_item[i], str) == True
                assert isinstance(rating[i], int)  == True



def data():

        rating_user, rating_item, rating = [], [], []

        for ind_file in range(2):
                rating_file_name = "part-"
                for ind_zero in range(5 - len(str(ind_file))):
                        rating_file_name += "0"
                rating_file_name += str(ind_file)
                rating_file = open('CI/dataset/' + rating_file_name, "r")
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

        return [rating_user, rating_item, rating]


