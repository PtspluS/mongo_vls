from flask import Flask, request, render_template
from markupsafe import escape
from functions import get_stations,find_station, delete_station, toggle_stations, edit_station, find_station_geo, \
    get_station_with_percent_between_days_and_hours_and_the_name_of_this_function_is_too_long, get_station
import pandas as pd

app = Flask("mongo_vls")

@app.route('/')
def hello_world():
    return render_template('index.html', stations=get_stations())

@app.route('/js.js')
def js():
    return render_template('js.js')


@app.route('/station/<stationname>',  methods=['GET', 'POST'])
def findstation(stationname):
    if request.method == 'POST':
        # find station with geoquery
        geojson = request.get_json()
        geojson = dict(geojson['geojson'])['features'][0]["geometry"]
        return render_template("view_station_list.html", stations=find_station_geo(geojson))
    else :
        return render_template("view_station_list.html", stations=find_station(escape(stationname)))

@app.route('/getstation/<id>')
def getstation(id):
    return get_station(escape(id))


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
    edit_station(id_station,station)
    return "", 204
     
@app.route('/ultra/<startday>/<endday>/<startime>/<endtime>/<percent>')
def ultra(startday, endday, startime, endtime, percent = 0.2):
    stations = get_station_with_percent_between_days_and_hours_and_the_name_of_this_function_is_too_long(startday, endday, startime, endtime, percent)
    return render_template("liste.html", liste=stations)


if __name__ == '__main__':
    app.run()