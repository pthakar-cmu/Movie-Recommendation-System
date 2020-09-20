# Movie Recommendation Project
Group 3 - Avengers

# Collect and clean data

This part includes collecting movie logs from 2020/7/29 to the most recent messages, reorganizing movie logs, and retrieving user and movie information. To run the files, see descriptions in each file about the commands and where they should be run. For the generated files in following steps, they are only test files that contain information from part of all messages.

### Collect data

In collect_and_clean_data/get_movie_log.py, we use Apache Kafka consumer to read streaming messages from the cluster. The server containing the stream and other APIs is 128.2.204.215. Here, we use a tunnel to establish connection with Apacha Kafka. Run `ssh -L 9092:localhost:9092 tunnel@128.2.204.215 -NT` in a new terminal window. In another terminal window, run `kafkacat -b localhost -L` to check out different partitions. For our group, we use partition movielog3. Results can be found in records.txt.

### Extract user ratings, user watch history, user and movie IDs from movie logs
Detailed information in clean_movie_log.py. Results are in KafkaData, users.txt and movies.txt.

### Retrieve user and movie information
Here, we use Scrapy to crawl web pages about user and movie info. Results are in user_info.txt and movie_info.txt. Further, user)info.txt is converted into .csv format (user_info.csv).


If surprise libarary is not installed, please install it first:
	
	pip3 install scikit-surprise

# Separate training and prediction

First, train the model with dataset once:

	python3 milestone1_training.py

It will generate a trained model file and combine all training data into a single file.

Then run predictions repeatly by accepting user ids:

	python3 milestone1_prediction.py [user_id]
	
It will print out recommended list of 20 movies
