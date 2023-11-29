import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import AutomapBase, automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:////Users/danielledubash/Desktop/Rice_Bootcamp/Homework_Assignment/Module10/Starter_Code/Resources/Hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
Measurements = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

#Variables
year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
#################################################
# Flask Setup
app = Flask(__name__)
#################################################

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start-end"
    )

#Convert the query results from your precipitation analysis 
@app.route("/api/v1.0/precipitation")
def precipitaions():
    """Return a list of all precipitation"""
    # Query all Precipitation
    oneyear = session.query(Measurements.date, Measurements.prcp).\
        filter(Measurements.date>year_ago).all()
    # Convert to dictionary, jsonify
    oneyeardict = dict(oneyear)
    return jsonify(oneyeardict)

#Return a JSON list of stations from the dataset
@app.route("/api/v1.0/stations")
def stations():
    stationlist = session.query(Station.station).all()
    stationlistdict = list(np.ravel(stationlist))
    return jsonify(stationlistdict)

#Return a JSON list of temperature observations for the previous year of the most active station.
@app.route("/api/v1.0/tobs")
def tobs():
    activestation = session.query(Measurements.date, Measurements.tobs).\
        filter(Measurements.station == 'USC00519281').\
        filter(Measurements.date>=year_ago).all()
    activestationdict = dict(activestation)
    return jsonify(activestationdict)

#Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start date
@app.route("/api/v1.0/start")
def start():
    # Minimum, maximum, and average temperature observed for provided start date
    start_stats = session.query(func.min(Measurements.tobs), func.max(Measurements.tobs),func.avg(Measurements.tobs)).\
        filter(Measurements.date >= dt.date(2017,8,23)).all()
    start_list = list(np.ravel(start_stats))
    return jsonify(start_list)

#Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start-end range
#app.route("api/v1.0/start-end")
#def startandend():


if __name__ == '__main__':
    app.run(debug=True)

session.close()