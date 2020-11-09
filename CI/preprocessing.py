# data preprocessing

import pandas as pd
import re
import json

def preprocess_data(num_file):

    rating_user, rating_item, rating = [], [], []

    for ind_file in range(num_file):
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

        #user_set = list(set(rating_user))
        movie_set = list(set(rating_item))

        with open('CI/movie_set.json', "w") as outfile:  
            json.dump(movie_set, outfile) 

    ratings_dict = {
        "item": rating_item,
        "user": rating_user,
        "rating": rating
    }

    # split dataset into traiing data and test data
    df = pd.DataFrame(ratings_dict)
    train_df = df.sample(frac=0.8, random_state=0)
    test_df = df.drop(train_df.index)
    
        
    return [train_df, test_df, df]