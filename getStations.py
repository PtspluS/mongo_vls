#!/usr/bin/env python3

import requests
import json
from pprint import pprint
from pymongo import MongoClient


def get_velib(url):
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    response_json = json.loads(response.text.encode('utf8'))
    return response_json.get("records", [])

def get_velyon(url):
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    response_json = json.loads(response.text.encode('utf8'))
    return response_json.get("values", [])

vlilles = get_velib(
    "https://opendata.lillemetropole.fr/api/records/1.0/search/?dataset=vlille-realtime&q=&rows=-1")
vLyon = get_velyon(
    "https://download.data.grandlyon.com/ws/rdata/jcd_jcdecaux.jcdvelov/all.json")
vParis = get_velib(
    "https://opendata.paris.fr/api/records/1.0/search/?dataset=velib-disponibilite-en-temps-reel&q=&rows=-1")
vRennes = get_velib(
    "https://data.rennesmetropole.fr/api/records/1.0/search/?dataset=stations_vls&q=&lang=fr&rows=-1")


# for vlib in vlilles + vParis + vLyon + vRennes:
#     print(json.dumps(vlib), end=",\n" )

vlilles_format = []
for vlib in vlilles:
    vlilles_format.append({
        "name": vlib["fields"]["nom"],
        "city": vlib["fields"]["commune"],
        "size": vlib["fields"]["nbvelosdispo"] + vlib["fields"]["nbplacesdispo"],
        "geo": vlib["geometry"],
        "TPE ": vlib["fields"]["type"] != "SANS TPE",
        "status": vlib["fields"]["etat"] == "EN SERVICE",
        "last update": vlib["record_timestamp"] })


vParis_format = []
for vlib in vParis:
    vParis_format.append({
        "name": vlib["fields"]["name"],
        "city": vlib["fields"]["nom_arrondissement_communes"],
        "size": vlib["fields"]["capacity"],
        "geo": vlib["geometry"],
        "TPE ": False,
        "status": vlib["fields"]["is_renting"] == 'OUI' and vlib["fields"]["is_returning"] == 'OUI',
        "last update": vlib["record_timestamp"] })

vLyon_format = []
for vlib in vLyon:
    vLyon_format.append({
        "name": vlib["name"],
        "city": vlib["commune"],
        "size": vlib["bike_stands"],
        "geo": {"type": "Point", "coordinates": [vlib["lng"], vlib["lat"]]},
        "TPE ": vlib["banking"],
        "status": vlib["status"] == "OPEN",
        "last update": vlib["last_update"] })

vRennes_format = []
for vlib in vRennes:
    vRennes_format.append({
        "name": vlib["fields"]["nom"],
        "city": "Rennes",
        "size": vlib["fields"]["nb_socles"],
        "geo": vlib["geometry"],
        "TPE ": vlib["fields"]["tpe"] == "oui",
        "status": vlib["fields"]["etat"] == 'Ouverte',
        "last update": vlib["record_timestamp"] })



print("Lille : " + str(len(vlilles_format)))
print("Paris : " + str(len(vParis_format)))
print("Lyon : " + str(len(vLyon_format)))
print("Rennes : " + str(len(vRennes_format)))

client = MongoClient('mongodb+srv://toto:toto@cluster0.eu1pi.mongodb.net/vls?retryWrites=true&w=majority')
db = client.vls  # or db = client['test-database']
collection = db.stations  # or collection = db['test-collection']

collection.create_index({ "geo" : "2dsphere" })

print("inserted : " + str(len(collection.insert_many(vlilles_format).inserted_ids)))
print("inserted : " + str(len(collection.insert_many(vParis_format).inserted_ids)))
print("inserted : " + str(len(collection.insert_many(vLyon_format).inserted_ids)))
print("inserted : " + str(len(collection.insert_many(vRennes_format).inserted_ids)))
