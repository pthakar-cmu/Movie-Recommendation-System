from kafka import KafkaConsumer
from json import loads

"""
To collect data, 
run 
    python3 collect_and_clean_data/get_movie_log.py 
in repo root (milestone1)
"""

# Create a consumer to read data from kafka
consumer = KafkaConsumer(
    # This is the movie log for Team 3
    'movielog3',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    # Consumer group id (*** Change this if you want to retrieve data from the beginning***)
    group_id='avengers-test12',
    # Commit that an offset has been read
    enable_auto_commit=True,
    # How often to tell Kafka, an offset has been read
    auto_commit_interval_ms=100
)

file = open('records.txt', 'w')
i = 0
# records = []
for message in consumer:
    i += 1
    file.write(message.value.decode('utf-8') + '\n')
    if i % 100000 == 0:
        print(i)
file.close()
print('Got first all movie logs!')
