import pyrebase
import os
from pymongo import MongoClient
from flask import request
import datetime
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

mongo_uri= 'mongodb+srv://cheliali:livelovelaugh@cluster0.raatz.mongodb.net/test'
db = MongoClient(host=mongo_uri).get_database()

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()
image="test10.jpg"

#Upload Image
#storage.child(image).put(image)

#Obtain URL
url=storage.child("oen apchagi").get_url(None)

users = db.users

'''users.update_one({'username': "cheliali"},
{"$push": {"history": {
"_id": ObjectId(),
"poomsae": 'poomsae 2',
"pose": 'are maki',
"grade": "90",
"date": datetime.datetime.utcnow(),
"picture": url,
"observations":
    'illum pariatur fugiat officia anim qui ut mollit irure nulla nisi officia et.',},}})'''


#Download Image
#storage.child(image).download(filename="oli.jpg", path=os.path.basename(image))

