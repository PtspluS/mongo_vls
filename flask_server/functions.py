#!/usr/bin/env python3

# User program: give available stations name next to the user lat, lon with last data (bikes and stand)

import requests
import json
from pprint import pprint
from pymongo import MongoClient, DESCENDING
from bson.objectid import ObjectId
from bson import json_util
import dateutil.parser
import re

client = MongoClient(
    'mongodb+srv://toto:toto@cluster0.eu1pi.mongodb.net/vls?retryWrites=true&w=majority')
db = client.vls  # or db = client['test-database']
collection_vlilles = db.vlilles  # or collection = db['test-collection']
collection_stations = db.stations  # or collection = db['test-collection']

# get a station from the id
def get_station(station_id):
    
    return json_util.dumps(collection_stations.find_one({"_id": ObjectId(station_id)}))

# find a station from a partial name
def find_station(name_partial: str):
    requete = {"name": re.compile(
        name_partial, re.IGNORECASE), "city": re.compile("Lille", re.IGNORECASE)}
    cursor = collection_stations.find(requete)
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
    station["_id"] = ObjectId(station["_id"])
    collection_stations.update_one({"_id": ObjectId(id_station)}, {
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


def get_station_with_percent_between_days_and_hours_and_the_name_of_this_function_is_too_long(start_day, end_day, start_time, end_time, percent=0.2):
    print("NOPE")
    request = [
        {"$match":{"status": True}},  # only look for the working stations
        {"$sort": {"record_timestamp": DESCENDING}}, # sort by date 
        {"$match":{    # time window to match 
            "$or": [  
                # hardcoded time of two days because the worker did not work for ever
                { "$and" : [ { "record_timestamp" : { "$lte" : dateutil.parser.parse(date+" "+ start_time + ".000Z")}} ,
                        { "record_timestamp" : { "$gte" : dateutil.parser.parse(date+" "+ end_time +".000Z")}} ]
                } for date in range(start_day, end_day)
                ]
        }},
        {"$project":  # Calculate the total of places can be done with an index I think but meh where is the fun
            {"_id":"$_id",
            "name": "$name",
                "total":{ "$add": ["$vlilles_dispo", "$places_dispo"]} , 
                "places_dispo" : "$places_dispo",
                "vlilles_dispo" : "$vlilles_dispo",
                "record_timestamp" : "$record_timestamp"
    }},
    {"$match":{"total": {"$gt": 0} }} , # avoid to get station with no total (cause blackhole later in the code /0)  
    {"$project": # calculate the percentage of bickes
            {"_id": "$_id", 
                "name": "$name", 
                "total": "$total", 
                "places_dispo" : "$places_dispo",
                "vlilles_dispo" : "$vlilles_dispo",  
                "percent" : {"$divide": [ "$vlilles_dispo" , "$total" ]},
                "record_timestamp" : "$record_timestamp"
    }},
    {"$match":{"percent": {"$lte": percent} }}, # Look for the percentage
    {"$group":  # we groupe by station name in order to extract it and the time where it was at 20%
            {"_id":"$name",
            "entries" : {"$push" : {
                "percent": "$percent",
                "places_dispo" : "$places_dispo",
                "vlilles_dispo" : "$vlilles_dispo",
                "record_timestamp" : "$record_timestamp"}
    }}},
    {"$project": # only get the _id because it's the station name that match all the previous
        { "_id":1 }},
    ]
    liste_station = collection_vlilles.aggregate(request)
    l = []
    pprint(request)
    for station in liste_station:
        l.append(station["_id"])
    return l