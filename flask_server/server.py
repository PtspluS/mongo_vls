from flask import Flask, request, render_template
from markupsafe import escape
from functions import find_station, delete_station
import pandas as pd

app = Flask("mongo_vls")

@app.route('/')
@app.route('/station/')
def hello_world():
    return render_template('index.html')

@app.route('/station/<stationname>')
def findstation(stationname):
    # show the user profile for that user
    return render_template("view_station_list.html", stations=find_station(escape(stationname)))


@app.route('/delete/<id_station>')
def delstation(id_station):
    # show the user profile for that 
    delete_station(escape(id_station))
    return "", 204
     



if __name__ == '__main__':
    app.run()