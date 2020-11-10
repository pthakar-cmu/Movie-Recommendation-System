from flask import Flask
from prediction import recommend, validate
import time

app = Flask(__name__)

resultGlobal = []

@app.route('/recommend/<userid>')
def index(userid):

    global resultGlobal

    start_time = round(time.time() * 1000)
    # Data Quality
    if not validate(test_user=userid):
        outputFileTrain.write(",,,Invalid")
        outputFileTrain.write('\n')
        return ""

    result = str(recommend(userid))

    # Collecting Online Telemetry
    outputFileTrain.write(str(start_time)+","+userid+","
                          +str(round(time.time() * 1000) - start_time)+","+result)
    outputFileTrain.write('\n')
    return result

if __name__ == '__main__':
    outputFileTrain = open("CI/logs.csv", "w")
    app.run( host="0.0.0.0", port=8082)
    outputFileTrain.close()