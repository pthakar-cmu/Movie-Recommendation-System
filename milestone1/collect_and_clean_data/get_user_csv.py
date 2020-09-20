import json
import pandas as pd
import requests
from time import sleep
import findspark
import pyspark
from pyspark.sql import SQLContext, Row

"""
This file converts user_info.txt into csv format.
Run python3 collect_and_clean_data/get_user_csv.py
"""

findspark.init()
sc = pyspark.SparkContext(appName="hw")
sqlContext = SQLContext(sc)
print("Spark context started")

# Read in text file
usersRDD = sc.textFile('get_user_movie_info/user_info.txt').cache()
usersJsonRDD = usersRDD.map(lambda info: json.loads(info)).cache()

# Check user info columns
assert(usersJsonRDD.filter(lambda info: len(info) != 4).count() == 0)

usersRows = usersJsonRDD.map(lambda info: Row(**info))
usersDF = usersRows.toDF().cache()
usersDF.toPandas().to_csv('user_info.csv', index=False) 
