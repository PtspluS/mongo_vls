from flask import Flask, request, render_template
from markupsafe import escape
from functions import find_station
import pandas as pd

app = Flask("mongo_vls")

@app.route('/')
@app.route('/station/')
def hello_world():
    return render_template('index.html')

@app.route('/station/<stationname>')
def findstation(stationname):
    # show the user profile for that user
    return "stations <br/> {} ".format( pd.DataFrame(find_station(escape(stationname))).groupby(['name']).sum().to_html())


if __name__ == '__main__':
    app.run()