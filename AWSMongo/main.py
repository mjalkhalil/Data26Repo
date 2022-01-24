import pymongo
import requests

client = pymongo.MongoClient("mongodb://3.70.205.189:27017/Sparta") # defaults to port 27017

db = client.Sparta


if __name__ == "__main__":
    db.data26.drop()
    db["data26"].insert_many([{"name": "Jad", "age": 24}, {"name": "Sandro"}])
    # print the number of documents in a collection
    print(db.list_collection_names())
    for each in db.data26.find():
        print(each)