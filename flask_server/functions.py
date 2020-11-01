#!/usr/bin/env python3

# User program: give available stations name next to the user lat, lon with last data (bikes and stand)

import requests
import json
from pprint import pprint
from pymongo import MongoClient, DESCENDING
import dateutil.parser
import re

client = MongoClient(
    'mongodb+srv://toto:toto@cluster0.eu1pi.mongodb.net/vls?retryWrites=true&w=majority')
db = client.vls  # or db = client['test-database']
collection_vlilles = db.vlilles  # or collection = db['test-collection']
collection_stations = db.stations  # or collection = db['test-collection']

# find a station from a partial name
def find_station(name_partial: str):
    requete = {"name": re.compile(
        name_partial, re.IGNORECASE), "city": re.compile("Lille", re.IGNORECASE)}
    cursor = collection_stations.find(requete)
    print("{} stations match".format(
        collection_stations.count_documents(requete)))
    l: list = []
    for i in cursor:
        l.append(i)
    return l

def find_station_geo(geojson):
    requete = {
        "city": re.compile("Lille", re.IGNORECASE),
        "geo": {
            "$geoWithin": {
                "$geometry": geojson
            }
        }
    }
    cursor = collection_stations.find(requete)
    print("{} stations match".format(
        collection_stations.count_documents(requete)))
    l: list = []
    for i in cursor:
        l.append(i)
    return l


def delete_station(name:str ):
    collection_vlilles.delete_many({"name": name})
    collection_stations.delete_many({"name": name})

def toggle_stations(state: bool, geojson : dict):
    geoquery = { 
        "geo": {
            "$geoWithin": {
                "$geometry": geojson
        }
    }}
    collection_stations.update_many(geoquery, {"$set": {"status": state}})
    stationlist = []
    for station in collection_stations.find(geoquery):
        stationlist.append(station)
    return stationlist


def edit_station(id_station,station):
    # Doesn't perform data sanitisation on user input
    # DB update
    collection_stations.update_one({"_id": id_station}, {
                                "$set": station})


def get_stations():
    cursor = collection_stations.aggregate([
    {"$match" :
        {"city": re.compile("Lille", re.IGNORECASE)}
    },
    { "$project" : {
        "name": "$name"
        }
    },])
    l = []
    for station in cursor :
        l.append(station["name"])
    return l

