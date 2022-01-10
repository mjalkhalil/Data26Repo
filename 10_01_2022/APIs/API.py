import requests
from pprint import pprint as pp

api_req = requests.get("https://api.publicapis.org/entries")

random_api = api_req.json()['entries'][:10]

for api in random_api:
    print(api['Link'])
    item = requests.get(api['Link'])
    print(type(item))
    pp(item.json())