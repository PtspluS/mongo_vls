#!/usr/bin/env python3

# User program: give available stations name next to the user lat, lon with last data (bikes and stand)

import requests
import json
from pprint import pprint
from pymongo import MongoClient, DESCENDING
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


# loop over asking for a value bewteen range
def input_range(min: int = 1, max: int = 5) -> int:
    while True:
        try:
            choix = input("choice [{},{}]:".format(min, max))
            choix = int(choix)
            if min <= choix <= max:
                return choix
        except:
            pass

# choose an item from a list


def input_list(liste: list) -> int:
    if len(liste) == 0:
        return -1
    if len(liste) == 1:
        input()
        return 0
    return input_range(0, len(liste)-1)


print("""
Choose one:
    1. find station with name (with some letters)
    2. update a stations
    3. delete a station and datas
    4. deactivate all station in an area
    5. give all stations with a ratio bike/total_stand under 20% between 18h and 19h00 (monday to friday)
""")

# Testing the input of the user
choix: int = input_range()

# choosing the options
if 1 <= choix <= 3:
    station_name = input("station name :")
    list_stations = find_station(station_name)
    for station in list_stations:
        pprint(station)
    if 2 <= choix <= 3:
        # choose a station to edit or delete
        print("\n\nchoose a station")
        [print("    " + str(indice) + " : " + value["name"])
         for indice, value in enumerate(list_stations)]
        station_to_edit: int = input_list(list_stations)
        if station_to_edit == -1:
            exit("no station found")
        station_to_edit: dict = list_stations[station_to_edit]
        
        if choix == 2 :
            print("\n\nGo for editing station {}".format(station_to_edit))
            pprint(station_to_edit)
            # Choose the field to edit
            [print("    " + str(key) + " : " + value + " : " + str(station_to_edit[value]))
            for key, value in enumerate(list(station_to_edit.keys())[1:])]
            print("\nfield to edit :")
            field_to_edit: int = input_list(list(station_to_edit.keys())[
                                            1:])  # 1: to avoid editing _id
            field_to_edit: str = list(station_to_edit.keys())[1:][field_to_edit]
            print("\n\nGo for editing field {}".format(field_to_edit))
            # edit the field and update the db
            value = input("new value of the field :")
            # DB update
            collection_stations.update_one({"_id": station_to_edit["_id"]}, {
                                        "$set": {field_to_edit: value}})

        if choix == 3 :
            # Deleting the station
            # First clean data
            collection_vlilles.delete_many({"name": station_to_edit["name"]})

            # Clean station
            collection_stations.delete_one(station_to_edit)

elif choix == 4:
    # disable Station in an area
    # get the area with geojson.io
    print("Draw your polygon geojson.io")
    geojson_file = input("geojson file :")
    geojson_file = json.loads(open(geojson_file).read().replace("\n",""))
    geoquery = { 
        "geo": {
            "$geoWithin": {
                "$geometry": geojson_file["features"][0]['geometry']
         }
    }}
    # pprint(geojson_file) # For debug
    cursor = collection_stations.find(geoquery)
    for station in cursor:
        pprint(station)
    
    while True:
        what_to_do = input("disable / enable (d/e):")
        if what_to_do == "e" or what_to_do == "d":
            break

    if what_to_do == "e":
        cursor = collection_stations.update_many(geoquery, {"$set": {"status": True}})
    elif what_to_do == "d":
        cursor = collection_stations.update_many(geoquery, {"$set": {"status": False}})
    else:
        pass

if choix == 5:
    # give all stations with a ratio bike/total_stand under 20% between 18h and 19h00 (monday to friday)
    collection_vlilles.agregate
else:
    pass