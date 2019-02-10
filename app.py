import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import datetime as dt
from datetime import datetime


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite?check_same_thread=False")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# We can view all of the classes that automap found
Base.classes.keys()

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)
#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    # Creating a landing page
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Createing a query to retrieve dates and precipitation values
    scores = session.query(Measurement.date, Measurement.prcp).all()
    
    # Converting the query results to a Dictionary
    precipitation = []
    for score in scores:
        precipitation_dict = {}
        precipitation_dict["date"] = score.date
        precipitation_dict["precipitation"] = score.prcp
        precipitation.append(precipitation_dict)
    return jsonify(precipitation)


@app.route("/api/v1.0/stations")
def stations():
    # Createing a query to retrieve  station values
    stations_query = session.query(Station.station).all()

    # Converting the query results to a Dictionary
    stations = []
    for station_val in stations_query:
        stations_dict = {}
        stations_dict["station"] = station_val.station
        stations.append(stations_dict)
    return jsonify(stations)
#     
@app.route("/api/v1.0/tobs")
def tobs():
    # Calculate latest date in the database
    latest_date = session.query(Measurement.date).first()
    # Convert latest_date string to a date object
    date_object = datetime.strptime(str(latest_date), "('%Y-%m-%d',)")
    # Calcuate one year ago from the latest date
    year_ago = date_object - dt.timedelta(days=365)
    # Createing a query to retrieve
    temp_obs_querry = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date > year_ago).all()
    
    # Converting the query results to a Dictionary
    temp_obs = []
    for obs in temp_obs_querry:
        temp_obs_dict = {}
        temp_obs_dict["date"] = obs.date
        temp_obs_dict["temp_bservation"] = obs.tobs
        temp_obs.append(temp_obs_dict)
    return jsonify(temp_obs)


@app.route("/api/v1.0/<start>")
def start_func(start):
    # Createing a query to retrieve max, min and avg temp observations for a givan date range
    start_temp_val = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
        .filter(Measurement.date >= start).all()
    start_date_temp = []
    
    # Converting the query results to a Dictionary
    for value in start_temp_val:
        start_date_temp_dict = {}
        start_date_temp_dict["min_temp"] = value[0]
        start_date_temp_dict["avg_temp"] = value[1]
        start_date_temp_dict["max_temp"] = value[2]
        start_date_temp.append(start_date_temp_dict)
    return jsonify(start_date_temp)
  
@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    # Createing a query to retrieve max, min and avg temp observations for a givan date range
    start_end_temp_val = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    
    # Converting the query results to a Dictionary 
    start_end_date_temp = []
    for val in start_end_temp_val:
        start_end_date_temp_dict = {}
        start_end_date_temp_dict["min_temp"] = val[0]
        start_end_date_temp_dict["avg_temp"] = val[1]
        start_end_date_temp_dict["max_temp"] = val[2]
        start_end_date_temp.append(start_end_date_temp_dict)
    return jsonify(start_end_date_temp)


if __name__ == '__main__':
    app.run(debug=True)
