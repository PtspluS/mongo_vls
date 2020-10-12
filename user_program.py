#!/usr/bin/env python3

# User program: give available stations name next to the user lat, lon with last data (bikes and stand)

import requests
import json
from pprint import pprint
from pymongo import MongoClient, DESCENDING


client = MongoClient('mongodb+srv://toto:toto@cluster0.eu1pi.mongodb.net/vls?retryWrites=true&w=majority')
db = client.vls # or db = client['test-database']
collection_vlilles = db.vlilles # or collection = db['test-collection']
collection_stations = db.stations # or collection = db['test-collection']


user_lng = input("your lng please :")
user_lat = input("your lat please :")



closest_station = collection_stations.find({
    "geo": {
     "$near": {
       "$geometry": {
          "type": "Point" ,
          "coordinates": [ float(user_lng) , float(user_lat) ]
       }
     }
   }})[0]


latest_data = collection_vlilles.find({
    "name" : closest_station["name"],
}).sort("record_timestamp", DESCENDING).next()

pprint(latest_data)