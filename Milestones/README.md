# Movie Recommendation Project
Group 3 - Avengers

## Collect and clean data

This part includes collecting movie logs from 2020/7/29 to the most recent messages, reorganizing movie logs, and retrieving user and movie information. For the generated files in following steps, they are only test files that contain information from part of all messages.

### Collect movie logs

In collect_and_clean_data/get_movie_log.py, we use Apache Kafka consumer to read streaming messages from the cluster. The server containing the stream and other APIs is 128.2.204.215. Here, we use a tunnel to establish connection with Apacha Kafka. Run `ssh -L 9092:localhost:9092 tunnel@128.2.204.215 -NT` in a new terminal window. In another terminal window, run `kafkacat -b localhost -L` to check out different partitions. For our group, we use partition movielog3. Results can be found in records.txt.

Run following commands to collect data.
	
	python3 collect_and_clean_data/get_movie_log.py 

### Extract user ratings, user watch history, user and movie IDs from movie logs
Detailed information in clean_movie_log.py. Results are in KafkaData, users.txt and movies.txt.

Run following commands to clean data.
	
	python3 collect_and_clean_data/clean_movie_log.py

### Retrieve user and movie information
Here, we use Scrapy to crawl web pages about user and movie info. Results are in user_info.txt and movie_info.txt. Further, user)info.txt is converted into .csv format (user_info.csv).

Run following commands in get_user_movie_info (outer) folder to collect user data.

	scrapy crawl userInfo

Run following commands in get_user_movie_info (outer) folder to collect movie data.

	scrapy crawl movieInfo

Run following commands to get .csv.
	
	python3 collect_and_clean_data/get_user_csv.py

