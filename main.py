from flask import Flask
from flask import Response
from flask import request
from flask import jsonify
from flask_cors import CORS, cross_origin
from pymongo import MongoClient
import certifi
import pyrebase
import os
import cv2
from bson import json_util

from blazepose import evaluate, iniciar, videostart, terminar
from dbcontroller import getposes

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS']='Content-Type'
app.config['TESTING'] = True

ca=certifi.where()

Flask.debug=False

global cap

#region MONGO
mongo_uri= 'mongodb+srv://cheliali:livelovelaugh@cluster0.raatz.mongodb.net/test'
db = MongoClient(host=mongo_uri, tlsCAFile=ca).get_database()
#endregion Mongo

#region Firebase
config = {
    "apiKey": "AIzaSyBAM7ePYf0GIulRbdZsLio1SdS6t6UGI4A",
    "authDomain": "first-skein-346416.firebaseapp.com",
    "databaseURL":"https://first-skein-346416.firebaseio.com",
    "projectId": "first-skein-346416",
    "storageBucket": "first-skein-346416.appspot.com",
    "messagingSenderId": "414119301715",
    "appId": "1:414119301715:web:370f9496c2237e0f226ca6",
    "measurementId": "G-K9QX1DERP4"
}
firebase = pyrebase.initialize_app(config)
storage = firebase.storage()
#endregion


@app.route("/login", methods=['POST'])
@cross_origin()
def login():
    users = db.users
    request_data = request.get_json()
    username = request_data['username']
    password = request_data['password']

    user=users.find_one({'username': username})

    if(user["password"]==password):

        return jsonify("ok")
    else:
        return jsonify("error")

@app.route("/register", methods=['POST'])
@cross_origin()
def register():
    users = db.users
    request_data = request.get_json()

    username = request_data['username']
    password = request_data['password']

    users.insert_one({'username': username, 'password': password})
    return jsonify("ok")

@app.route("/getpoomsaeposes", methods=['GET'])
@cross_origin()
def poomsae1():
    poses=getposes()
    return poses

@app.route("/iniciar", methods=['GET'])
@cross_origin()
def iniciarf():
    global userid
    global posename
    arguments=request.args
    userid=arguments.get('userid')
    posename=arguments.get('pose')
    resp = iniciar(userid,posename)
    return jsonify(resp)

@app.route("/video_feed")
def video_feed():
    global cap
    if os.environ.get('WERKZEUG_RUN_MAIN') or Flask.debug is False:
        cap = cv2.VideoCapture(0)
    return Response(videostart(cap),
    mimetype = "multipart/x-mixed-replace; boundary=frame")

@app.route("/terminar", methods=['GET'])
@cross_origin()
def terminarf():
    terminar()
    return jsonify("ok")

@app.route("/evaluate", methods=['GET'])
@cross_origin()
def evaluation():
    finalGrade = evaluate()
    return jsonify(finalGrade)

@app.route("/getHistory", methods=['GET'])
@cross_origin()
def getHistory():
    history=[]
    users = db.users
    arguments=request.args
    userid=arguments.get('userid')

    user=users.find_one({'username': userid})

    if user:
        history=user['history']

    # return jsonify(history)
    return Response(
        json_util.dumps(history),
        mimetype='application/json'
    )

if __name__ == "__main__":
    app.run(debug=False)