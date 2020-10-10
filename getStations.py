import requests
import json
from pymongo import MongoClient


def get_velib(url):
    payload = {}
    headers= {}
    response = requests.request("GET", url, headers=headers, data = payload)
    response_json = json.loads(response.text.encode('utf8'))
    return response_json.get("records", [])

def get_velib_Lyon(url):
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data = payload)
    response_json = json.loads(response.text.encode('utf8'))
    return response_json.get("values", [])




vlilles = get_velib("https://opendata.lillemetropole.fr/api/records/1.0/search/?dataset=vlille-realtime&q=&rows=300&facet=libelle&facet=nom&facet=commune&facet=etat&facet=type&facet=etatconnexion")
vLyon = get_velib_Lyon("https://download.data.grandlyon.com/ws/grandlyon/pvo_patrimoine_voirie.pvostationvelov/all.json?maxfeatures=427&start=1")
vParis = get_velib("https://opendata.paris.fr/api/records/1.0/search/?dataset=velib-disponibilite-en-temps-reel&q=&rows=-1&facet=name&facet=is_installed&facet=is_renting&facet=is_returning&facet=nom_arrondissement_communes")
vRennes = get_velib("https://data.rennesmetropole.fr/api/records/1.0/search/?dataset=stations_vls&q=&lang=fr&rows=-1")


for vlille in vlilles:
    print(json.dumps(vlille), end=",\n" )

for vParis_ in vParis:
    print(json.dumps(vParis_),end=',\n')

for vLyon_ in vLyon:
    print(json.dumps(vLyon_),end=',\n')

for vRennes_ in vRennes:
    print(json.dumps(vRennes_),end=',\n')


client = MongoClient('mongodb://localhost:27017/')
db = client.vls # or db = client['test-database']
collection = db.stations # or collection = db['test-collection']

collection.insert_many(vlilles)
collection.insert_many(vParis)
collection.insert_many(vLyon)
collection.insert_many(vRennes)