#!/usr/bin/env python3

# Worker who refresh and store live data for a city (history data)
# We choose lille

import requests
import json
from pprint import pprint
from pymongo import MongoClient, errors
import datetime

client = MongoClient('mongodb+srv://toto:toto@cluster0.eu1pi.mongodb.net/vls?retryWrites=true&w=majority')
db = client.vls # or db = client['test-database']
collection_vlilles = db.vlilles # or collection = db['test-collection']

#collection_vlilles.create_index([('name',1), ('record_timestamp',-1)], unique=True)

def get_velib(url):
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    response_json = json.loads(response.text.encode('utf8'))
    return response_json.get("records", [])


vlilles = get_velib(
    "https://opendata.lillemetropole.fr/api/records/1.0/search/?dataset=vlille-realtime&q=&rows=-1")


vlilles_format = []
for vlib in vlilles:
    vlilles_format.append({
        "name": vlib["fields"]["nom"],
        "vlilles_dispo": vlib["fields"]["nbvelosdispo"],
        "places_dispo" : vlib["fields"]["nbplacesdispo"],
        "status": vlib["fields"]["etat"] == "EN SERVICE",
        "record_timestamp": datetime.datetime.fromisoformat(vlib["record_timestamp"]) })

try:
    print("inserted : " + str(len(collection_vlilles.insert_many(vlilles_format, ordered=False).inserted_ids)))
except errors.BulkWriteError as e:
    pass
