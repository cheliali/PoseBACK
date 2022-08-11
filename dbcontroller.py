from pymongo import MongoClient
from bson.json_util import dumps
from flask import request
from bson.objectid import ObjectId
import datetime

mongo_uri= 'mongodb+srv://cheliali:livelovelaugh@cluster0.raatz.mongodb.net/test'
db = MongoClient(host=mongo_uri).get_database()

def getuser():
    
    request_data = request.get_json()

    username = request_data['username']
    password = request_data['password']

    return username, password

def getposes():

    cursor=db.poomsaes.find()
    poseslist=list(cursor)

    for poomsae in poseslist:
        poomsae['_id'] = str(poomsae['_id'])

    json_poses=dumps(poseslist)

    return json_poses

''' def posthistory(username):
    
    users = db.users
    users.update_one({'username': username},
     {"$push": {"history": {
     "_id": ObjectId(),
     "poomsae": 'poomsae 2',
     "pose": 'are maki',
     "grade": "90",
     "date": datetime.datetime.utcnow(),
     "picture": url,
     "observations":
     'illum pariatur fugiat officia anim qui ut mollit irure nulla nisi officia et.',},}})   '''