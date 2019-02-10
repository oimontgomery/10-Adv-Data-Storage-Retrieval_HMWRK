import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

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
def welcome():
    #"""List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitations():
    #Query for the dates and temperature observations from the last year.
    obs = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date.between('2016-08-23','2017-08-23')).order_by(Measurement.date.asc()).all()

    all_precipitation = []

    for precipitation in obs:
        precipitation_dict = {}
        precipitation_dict["date"]= precipitation.date
        precipitation_dict["precipitation"] = precipitation.prcp
        all_precipitation.append(precipitation_dict)
    return jsonify(all_precipitation)

@app.route("/api/v1.0/stations")
def stations():
    #Return a JSON list of stations from the dataset.
    stations = session.query(Station.id, Station.station).all()

    all_stations = []

    for station in stations:
        station_dict = {}
        station_dict["station id"] = station.id
        station_dict["station name"] = station.station
        all_stations.append(station_dict)
    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def temp():
    #Return a JSON list of Temperature Observations (tobs) for the previous year.
    temps = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date.between('2016-08-23','2017-08-23')).order_by(Measurement.date.asc()).all()

    all_temp = []

    for temp in temps:
        temp_dict = {}
        temp_dict["date"]= temp.date
        temp_dict["temperature"] = temp.tobs
        all_temp.append(temp_dict)
    return jsonify(all_temp)


#Return a JSON list of the minimum temperature, the average temperature, and the max temperature 
#for a given start or start-end range.

@app.route("/api/v1.0/<start>")
#When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.

def start_data(start):

    start_temps = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date.between(start,'2017-08-23')).all()
    
    temps = [start_temp[1] for start_temp in start_temps]

    min_temps = min(temps)
    max_temps = max(temps)
    avg_temps = np.mean(temps)

    return jsonify(min_temps, max_temps, avg_temps)

    
@app.route("/api/v1.0/<start>/<end>")

def start_end_data(start,end):
    
    end_temps = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date.between(start,end)).all()

    temps = [end_temp[1] for end_temp in end_temps]
    
    min_temps = min(temps)
    max_temps = max(temps)
    avg_temps = np.mean(temps)

    return jsonify(min_temps, max_temps, avg_temps) 

if __name__ == '__main__':
    app.run(debug=True)