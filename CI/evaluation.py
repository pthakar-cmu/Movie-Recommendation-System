# evaluate the model offline

from random import randint,sample
import pandas as pd
import json
import sys
from collections import defaultdict


def validate(test_user):
  try:
    int(test_user)
    return True
  except:
    return False

def read_json(name):
  with open(name) as f:
    data = json.load(f)
  return data

def evaluate_model_offline(test_user):
    movie_list = read_json('CI/movie_set.json')
    prediction_data = read_json('CI/final_prediction.json')

    result = []
    if str(test_user) in prediction_data:
        print("find it")
        result = prediction_data[str(test_user)]
    else:
        print("random")
        result = sample(movie_list,20)
    print(",".join(result))




def precision_recall_at_k(predictions, k=20, threshold=3.5, epsilon=1e-7):
    """
    Return precision and recall at k metrics for each user. 
    Modified from https://surprise.readthedocs.io/en/stable/FAQ.html#how-to-compute-precision-k-and-recall-k
    """
    print('Calculating metrics')
    # First map the predictions to each user.
    user_est_true = defaultdict(list)
    for uid, _, true_r, est, _ in predictions:
        user_est_true[uid].append((est, true_r))

    metrics = {'user_id': [], 'precision': [], 'recall': [], 'f1': []}
    for uid, user_ratings in user_est_true.items():
        
        # Sort user ratings by estimated value
        user_ratings.sort(key=lambda x: x[0], reverse=True)

        # Number of relevant items
        n_rel = sum((true_r >= threshold) for (_, true_r) in user_ratings)

        # Number of recommended items in top k
        n_rec_k = sum((est >= threshold) for (est, _) in user_ratings[:k])

        # Number of relevant and recommended items in top k
        n_rel_and_rec_k = sum(((true_r >= threshold) and (est >= threshold))
                              for (est, true_r) in user_ratings[:k])

        # Precision@K: Proportion of recommended items that are relevant
        # When n_rec_k is 0, Precision is undefined. We here set it to 0.

        precision = n_rel_and_rec_k / n_rec_k if n_rec_k != 0 else 0

        # Recall@K: Proportion of relevant items that are recommended
        # When n_rel is 0, Recall is undefined. We here set it to 0.

        recall = n_rel_and_rec_k / n_rel if n_rel != 0 else 0

        # Add f1 score here
        f1 = 2 * precision * recall / (precision + recall + epsilon)

        metrics['user_id'].append(uid)
        metrics['precision'].append(precision)
        metrics['recall'].append(recall)
        metrics['f1'].append(f1)

    return metrics


def age_group(num):
    if num <= 20:
        return '0-20'
    elif num <= 35:
        return '21-35'
    elif num <= 50:
        return '36-50'
    else:
        return '51+'


def get_metrics_summary(metrics, user_info, output, score='f1'):
    if score not in ['f1', 'precision', 'recall']:
        print('Please choose a valid metric (f1, precision, recall)!')
    print('Summarizing metrics')
    users = pd.read_csv(user_info)
    metrics = pd.DataFrame(metrics)
    df = pd.merge(metrics, users, how='left', on='user_id')
    mean_score = df[score].mean()
    genders = df[['gender', score]].groupby(['gender']).mean().reset_index().to_dict('split')['data']
    df['age_group'] = df['age'].apply(age_group)
    ages = df[['age_group', score]].groupby(['age_group']).mean().reset_index().to_dict('split')['data']
    write_offline_metrics_report(score, mean_score, genders, ages, output)


def write_offline_metrics_report(score, mean_score, gender_score, age_score, output):
    with open(output, 'w') as file:
        file.write('********** Offline Metric Report **********')
        file.write('\n\n')
        file.write('Mean ' + score + ' Score: ' + str(mean_score))
        file.write('\n\n')
        file.write('Group by Gender\n')
        for row in gender_score:
            file.write(row[0] + ': \t' + str(row[1]) + '\n')
        file.write('\n')
        file.write('Group by Age\n')
        for row in age_score:
            file.write(row[0] + ': \t' + str(row[1]) + '\n')
        file.write('\n')


def get_top_n(predictions, n=20):
    """
    Return the top-N recommendation for each user from a set of predictions.
    Modified from https://surprise.readthedocs.io/en/stable/FAQ.html#how-to-get-the-top-n-recommendations-for-each-user
    Args:
        predictions(list of Prediction objects): The list of predictions, as returned by the test method of an algorithm.
        n(int): The number of recommendation to output for each user. Default is 20.
    Returns:
    A dict where keys are user (raw) ids and values are lists of tuples:
        [(raw item id, rating estimation), ...] of size n.
    """

    # First map the predictions to each user.
    top_n = defaultdict(list)
    for uid, iid, true_r, est, _ in predictions:
        top_n[uid].append((iid, est))

    # Then sort the predictions for each user and retrieve the k highest ones.
    for uid, user_ratings in top_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        top_n[uid] = [r[0] for r in user_ratings[:n]]

    return top_n