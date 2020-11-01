from flask import Flask, request, render_template
from markupsafe import escape
from functions import get_stations,find_station, delete_station, toggle_stations, edit_station, find_station_geo
import pandas as pd

app = Flask("mongo_vls")

@app.route('/')
def hello_world():
    return render_template('index.html', stations=get_stations())


@app.route('/station/<stationname>',  methods=['GET', 'POST'])
def findstation(stationname):
    print(request.method == 'POST')
    if request.method == 'POST':
        # find station with geoquery
        geojson = request.get_json()
        geojson = dict(geojson['geojson'])['features'][0]["geometry"]
        return render_template("view_station_list.html", stations=find_station_geo(geojson))
    else :
        return render_template("view_station_list.html", stations=find_station(escape(stationname)))


@app.route('/delete/<id_station>')
def delstation(id_station):
    delete_station(escape(id_station))
    return "", 204
     


@app.route('/toggle/<state>', methods=['POST'])
def toggle_station(state):
    state = escape(state) == "true"
    geojson = request.get_json()
    geojson = dict(geojson['geojson'])['features'][0]["geometry"]
    # print(geojson)
    stations = toggle_stations(state,geojson)
    # print(stations)
    return render_template("view_station_list.html", stations=stations)
     

@app.route('/edit/<id_station>', methods=['POST'])
def editstation(id_station):
    station = request.get_json()
    # print(geojson)
    edit_station(id_station,station)
    # print(stations)
    return "", 204
     



if __name__ == '__main__':
    app.run()