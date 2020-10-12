import requests
import json
from pymongo import MongoClient


def get_velib(url):
    payload = {}
    headers= {}
    response = requests.request("GET", url, headers=headers, data = payload)
    response_json = json.loads(response.text.encode('utf8'))
    return response_json.get("records", [])



vlilles = get_velib("https://opendata.lillemetropole.fr/api/records/1.0/search/?dataset=vlille-realtime&q=&rows=-1")
vLyon = get_velib("https://public.opendatasoft.com/api/records/1.0/search/?dataset=station-velov-grand-lyon&q=&rows=-1")
vParis = get_velib("https://opendata.paris.fr/api/records/1.0/search/?dataset=velib-disponibilite-en-temps-reel&q=&rows=-1")
vRennes = get_velib("https://data.rennesmetropole.fr/api/records/1.0/search/?dataset=stations_vls&q=&lang=fr&rows=-1")


# for vlille in vlilles:
#     print(json.dumps(vlille), end=",\n" )

# for vParis_ in vParis:
#     print(json.dumps(vParis_),end=',\n')

# for vLyon_ in vLyon:
#     print(json.dumps(vLyon_),end=',\n')

# for vRennes_ in vRennes:
#     print(json.dumps(vRennes_),end=',\n')

print("Lille : "+ str(len(vlilles)))
print("Paris : "+ str(len(vParis)))
print("Lyon : "+ str(len(vLyon)))
print("Rennes : "+ str(len(vRennes)))

client = MongoClient('mongodb://localhost:27017/')
db = client.vls # or db = client['test-database']
collection = db.stations # or collection = db['test-collection']

print("inserted : " + str(len(collection.insert_many(vlilles).inserted_ids)))
print("inserted : " + str(len(collection.insert_many(vParis).inserted_ids)))
print("inserted : " + str(len(collection.insert_many(vLyon).inserted_ids)))
print("inserted : " + str(len(collection.insert_many(vRennes).inserted_ids)))


