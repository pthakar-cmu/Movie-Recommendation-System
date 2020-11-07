from flask import Flask
from milestone1_prediction import recommend
app = Flask(__name__)


# @app.route('/h')
# def index():
#     return "Hello"

resultGlobal = []

@app.route('/recommend/<userid>')
def index(userid):

    global resultGlobal

    return str(recommend(userid, resultGlobal))

if __name__ == '__main__':
    print("Hey There")
    resultGlobal = readFile()
    app.run( host="0.0.0.0", port="8082")

