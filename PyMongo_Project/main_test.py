from main import *
from bson import objectid

data = {'count': 36,
 'next': None,
 'previous': None,
 'results': [{'MGLT': '60',
              'cargo_capacity': '3000000',
              'consumables': '1 year',
              'cost_in_credits': '3500000',
              'created': '2014-12-10T14:20:33.369000Z',
              'crew': '30-165',
              'edited': '2014-12-20T21:23:49.867000Z',
              'films': ['https://swapi.dev/api/films/1/',
                        'https://swapi.dev/api/films/3/',
                        'https://swapi.dev/api/films/6/'],
              'hyperdrive_rating': '2.0',
              'length': '150',
              'manufacturer': 'Corellian Engineering Corporation',
              'max_atmosphering_speed': '950',
              'model': 'CR90 corvette',
              'name': 'CR90 corvette',
              'passengers': '600',
              'pilots': [],
              'starship_class': 'corvette',
              'url': 'https://swapi.dev/api/starships/2/'}]}
result = [{'MGLT': '60',
              'cargo_capacity': '3000000',
              'consumables': '1 year',
              'cost_in_credits': '3500000',
              'created': '2014-12-10T14:20:33.369000Z',
              'crew': '30-165',
              'edited': '2014-12-20T21:23:49.867000Z',
              'films': ['https://swapi.dev/api/films/1/',
                        'https://swapi.dev/api/films/3/',
                        'https://swapi.dev/api/films/6/'],
              'hyperdrive_rating': '2.0',
              'length': '150',
              'manufacturer': 'Corellian Engineering Corporation',
              'max_atmosphering_speed': '950',
              'model': 'CR90 corvette',
              'name': 'CR90 corvette',
              'passengers': '600',
              'pilots': [],
              'starship_class': 'corvette',
              'url': 'https://swapi.dev/api/starships/2/'}]
pilots_t = [{"_id": objectid.ObjectId("61e93a374894dae4cdfb2b52"),
             "name":"Belbullab-22 starfighter",
             "model":"Belbullab-22 starfighter",
             "manufacturer":"Feethan Ottraw Scalable Assemblies",
             "cost_in_credits":"168000",
             "length":"6.71",
             "max_atmosphering_speed":"1100",
             "crew":"1",
             "passengers":"0",
             "cargo_capacity":"140",
             "consumables":"7 days",
             "hyperdrive_rating":"6",
             "MGLT":"unknown",
             "starship_class":"starfighter",
             "pilots":["https://swapi.dev/api/people/10/","https://swapi.dev/api/people/79/"],
             "films":["https://swapi.dev/api/films/6/"],
             "created":"2014-12-20T20:38:05.031000Z",
             "edited":"2014-12-20T21:23:49.959000Z",
             "url":"https://swapi.dev/api/starships/74/"}]
pilots_t2 = [{"_id": objectid.ObjectId("61e93a374894dae4cdfb2b52"),
             "name":"Belbullab-22 starfighter",
             "model":"Belbullab-22 starfighter",
             "manufacturer":"Feethan Ottraw Scalable Assemblies",
             "cost_in_credits":"168000",
             "length":"6.71",
             "max_atmosphering_speed":"1100",
             "crew":"1",
             "passengers":"0",
             "cargo_capacity":"140",
             "consumables":"7 days",
             "hyperdrive_rating":"6",
             "MGLT":"unknown",
             "starship_class":"starfighter",
             "pilots":[],
             "films":["https://swapi.dev/api/films/6/"],
             "created":"2014-12-20T20:38:05.031000Z",
             "edited":"2014-12-20T21:23:49.959000Z",
             "url":"https://swapi.dev/api/starships/74/"}]
ids_t = [objectid.ObjectId('61e6a4322db630197dac16e5'), objectid.ObjectId('61e6a425e18b89b3c7943de2')]


def test_get_data():
    assert get_data(data) == result

def test_get_ids():
    assert get_ids(pilots_t) == ids_t
    assert get_ids(pilots_t2) == []

def test_add_to_database():
    db.starships.drop()
    add_to_database(data)
    for each in db.starships.find({"name":"Belbullab-22 starfighter"}, {"cost_in_credits":1, "_id":0}):
        assert each == data["results"][0]["cost_in_credits"]

def test_delete_starship():
    for ss in db.starships.find({"name": "CR90 corvette"}, {"_id": 1}):
        test_id = str(ss["_id"])
        delete_starship(test_id)
        for each in db.starships.find({"_id": ss["_id"]}):
            assert each is None