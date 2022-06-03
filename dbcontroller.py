from pymongo import MongoClient
from bson.json_util import dumps

mongo_uri= 'mongodb+srv://cheliali:livelovelaugh@cluster0.raatz.mongodb.net/test'
db = MongoClient(host=mongo_uri).get_database()

def getposes():

    cursor=db.poomsaes.find()
    poseslist=list(cursor)

    for poomsae in poseslist:
        poomsae['_id'] = str(poomsae['_id'])

    json_poses=dumps(poseslist)

    return json_poses