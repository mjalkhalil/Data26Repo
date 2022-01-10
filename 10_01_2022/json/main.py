import json
import pyodbc

car_data = [{"name": "tesla", "engine": "electric"},
            {"name": "toyota", "engine": "petrol"},
            {"name": "mazda", "engine": "diesel"}]

car_data_json = json.dumps(car_data)
print(car_data_json)

with open("new_json_file.json", 'w') as f:
    json.dump(car_data, f)

with open("new_json_file.json", 'r') as f:
    car = json.load(f)
    print(car)