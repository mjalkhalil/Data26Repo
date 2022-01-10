import requests
from pprint import pprint as pp

postcodes = ["NW89PN", "NW65HT", "CO43SQ"]

post_codes_req = requests.post("http://api.postcodes.io/postcodes", json= {'postcodes': postcodes})

for i in range(len(postcodes)):
    pp(post_codes_req.json()['result'][i]['result']['postcode'])

for postcode in postcodes:
    post_codes_req = requests.get(f"http://api.postcodes.io/postcodes/{postcode}")
    print(post_codes_req.json()['result']['postcode'])