from flask import Flask
from milestone1_prediction import recommend, validate
import time
from milestone1_prediction import read_json

app = Flask(__name__)

resultGlobal = []
movie_list = read_json('movie_set.json')
prediction_data = read_json('final_prediction.json')

@app.route('/recommend/<userid>')
def index(userid):

    global resultGlobal

    start_time = round(time.time() * 1000)
    # Data Quality
    if not validate(test_user=userid):
        outputFileTrain.write(",,,Invalid")
        outputFileTrain.write('\n')
        return ""

    result = str(recommend(userid, movie_list, prediction_data))

    # Collecting Online Telemetry
    outputFileTrain.write(str(start_time)+","+userid+","
                          +str(round(time.time() * 1000) - start_time)+","+result)
    outputFileTrain.write('\n')
    return result

if __name__ == '__main__':
    outputFileTrain = open("logs.csv", "w")
    app.run( host="0.0.0.0", port=8082)
    outputFileTrain.close()

