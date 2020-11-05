from flask import Flask
from milestone1_prediction import recommend
app = Flask(__name__)


# @app.route('/h')
# def index():
#     return "Hello"



@app.route('/recommend/<userid>')
def index(userid):
    return str(recommend(userid))

if __name__ == '__main__':
    app.run( host="0.0.0.0", port="8082")

