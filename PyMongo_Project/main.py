import pymongo
import requests

def get_data(api):
    starships = []
    while api["next"] != None:
        for each in api["results"]:
            starships.append(each)
        new = requests.get(api["next"])
        api = new.json()
        if api["next"] == None:
            for each in api["results"]:
                starships.append(each)
    return starships

def get_ids(database):
    for pilot in database:
        if pilot["pilots"] != []:
            ids = []
            for each in pilot["pilots"]:
                pilot_api = requests.get(each)
                pilot_json = pilot_api.json()
                pilot_id = db.characters.find({"name": pilot_json["name"]}, {"_id": 1})
                for each in pilot_id:
                    ids.append(each["_id"])
            db.starships.update_one({"_id": pilot["_id"]},
                                    {"$set":
                                         {"pilots": ids}})

client = pymongo.MongoClient()
db = client['starwars']
db.starships.drop()

swapi = requests.get("https://swapi.dev/api/starships/?page=1")
swapi_api = swapi.json()

db["starships"].insert_many(get_data(swapi_api))

pilots = db.starships.find()

get_ids(pilots)
