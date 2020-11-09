from flask import Flask
from evaluation import evaluate_model_offline, validate
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

    result = str(evaluate_model_offline(userid))

    # Collecting Online Telemetry
    outputFileTrain.write(str(start_time)+","+userid+","
                          +str(round(time.time() * 1000) - start_time)+","+result)
    outputFileTrain.write('\n')
    return result

if __name__ == '__main__':
    outputFileTrain = open("CI/logs.csv", "w")
    app.run( host="0.0.0.0", port=8082)
    outputFileTrain.close()