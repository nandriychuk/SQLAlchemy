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
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

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

@app.route("/api/v1.0/precipitation")
def precipitation():
    scores = session.query(Measurement.date, Measurement.prcp).all()
    
    precipitation = []
    for score in scores:
        precipitation_dict = {}
        precipitation_dict["date"] = score.date
        precipitation_dict["precipitation"] = score.prcp
        precipitation.append(precipitation_dict)
    return jsonify(precipitation)


@app.route("/api/v1.0/stations")
def stations():
    stations = session.query(Station.station).all()
    
    return jsonify(stations)
#     return (
#         f"Available Routes:<br/>"
#         f"/api/v1.0/names<br/>"
#         f"/api/v1.0/passengers"
# #     )
@app.route("/api/v1.0/tobs")
def tobs():
    latest_date = session.query(Measurement.date).first()
# Convert latest_date string to a date object
    date_object = datetime.strptime(str(latest_date), "('%Y-%m-%d',)")
# Calcuate one year ago from the latest date
    year_ago = date_object - dt.timedelta(days=365)
    temp_obs = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date > year_ago).all()
    
    return jsonify(temp_obs)

@app.route("/api/v1.0/<start>")
def start(start):
    def calc_temps(start_date, end_date):
    # """TMIN, TAVG, and TMAX for a list of dates.
    # Args:
    #     start_date (string): A date string in the format %Y-%m-%d
    #     end_date (string): A date string in the format %Y-%m-%d       
    # Returns:
    #     TMIN, TAVE, and TMAX
    # """
        return jsonify(session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all())

    # latest_date = session.query(Measurement.date).first()
    output = calc_temps(start, "2017-08-23")
    return output    
    # year_ago = date_object - dt.timedelta(days=365)
    # temp_obs = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date > year_ago).all()
    
@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    def calc_temps(start_date, end_date):
    # """TMIN, TAVG, and TMAX for a list of dates.
    # Args:
    #     start_date (string): A date string in the format %Y-%m-%d
    #     end_date (string): A date string in the format %Y-%m-%d       
    # Returns:
    #     TMIN, TAVE, and TMAX
    # """
        return jsonify(session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all())

    # latest_date = session.query(Measurement.date).first()
    output = calc_temps(start, end)
    return output   





# @app.route("/api/v1.0/names")
# def names():
#     """Return a list of all passenger names"""
#     # Query all passengers
#     results = session.query(Passenger.name).all()

#     # Convert list of tuples into normal list
#     all_names = list(np.ravel(results))

#     return jsonify(all_names)


# @app.route("/api/v1.0/passengers")
# def passengers():
#     """Return a list of passenger data including the name, age, and sex of each passenger"""
#     # Query all passengers
#     results = session.query(Passenger).all()

#     # Create a dictionary from the row data and append to a list of all_passengers
#     all_passengers = []
#     for passenger in results:
#         passenger_dict = {}
#         passenger_dict["name"] = passenger.name
#         passenger_dict["age"] = passenger.age
#         passenger_dict["sex"] = passenger.sex
#         all_passengers.append(passenger_dict)

#     return jsonify(all_passengers)


if __name__ == '__main__':
    app.run(debug=True)
