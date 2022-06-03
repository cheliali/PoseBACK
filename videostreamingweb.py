from flask import Flask
from flask import request
from flask import render_template
from flask import Response
from flask import jsonify
from flask_cors import CORS, cross_origin
from pymongo import MongoClient

from blazepose import iniciar, videostart, terminar
from dbcontroller import getposes

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS']='Content-Type'
app.config['TESTING'] = True

mongo_uri= 'mongodb+srv://cheliali:livelovelaugh@cluster0.raatz.mongodb.net/test'
db = MongoClient(host=mongo_uri).get_database()

@app.route("/iniciar", methods=['GET'])
@cross_origin()
def iniciarf():
     iniciar()
     return jsonify("ok")

@app.route("/video_feed")
def video_feed():
     return Response(videostart(),
          mimetype = "multipart/x-mixed-replace; boundary=frame")

@app.route("/terminar", methods=['GET'])
@cross_origin()
def terminarf():
     terminar()
     return jsonify("ok")

@app.route("/register", methods=['POST'])
@cross_origin()
def register():
     users = db.users
     request_data = request.get_json()

     username = request_data['username']
     password = request_data['password']

     users.insert_one({'username': username, 'password': password})
     return jsonify("ok")

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

@app.route("/getpoomsaeposes", methods=['GET'])
@cross_origin()
def poomsae1():
     poses=getposes()
     return poses

if __name__ == "__main__":
     app.run(debug=True)

