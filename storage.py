import pyrebase
import os
from pymongo import MongoClient
from flask import request
import datetime
import json
from bson.objectid import ObjectId

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

with open('/home/pi/Desktop/history.json', 'rb') as f:
    history = json.load(f)

mongo_uri= 'mongodb+srv://cheliali:livelovelaugh@cluster0.raatz.mongodb.net/test'
db = MongoClient(host=mongo_uri).get_database()
users = db.users

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()
user=history["username"]
pose=history["pose"]
date=str(datetime.datetime.utcnow())
calificaciones=history["calificacionesInd"]
image="/home/pi/Desktop/finalIm.jpg"
dir=user+"/"+pose+"/"+date

def createHistory():

    storage.child(dir).put(image)
    url=storage.child(dir).get_url(None)

    users.update_one({'username': user},
    {"$push": {"history": {
    "_id": ObjectId(),
    "poomsae": 'Poomsae 1',
    "pose": pose,
    "date": date,
    "picture": url,
    "observations":
        calificaciones,},}})


#Download Image
#storage.child(image).download(filename="oli.jpg", path=os.path.basename(image))

# uploadImageFirebase()
createHistory()