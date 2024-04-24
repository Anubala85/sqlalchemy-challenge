# Import the dependencies.
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import and_
from sqlalchemy import desc
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
Station = Base.classes.station
Measurement = Base.classes.measurement

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


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
        f"/api/v1.0/startdate<br/>"
        f"/api/v1.0/startdate/enddate<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    #Fetching Precipitation Details for Last 12 months
    session = Session(engine)
    
    #Calculating start and end dates and transforming them to datetime formats
    most_recent_date_str = session.query (Measurement.date).order_by(Measurement.date.desc()).first()
    end_date = dt.datetime.strptime (most_recent_date_str[0], '%Y-%m-%d')
    start_date = end_date - dt.timedelta (days = 366)
    
    prcp_scores = session.query (Measurement.date, Measurement.prcp).\
        filter (and_
                (Measurement.date >= start_date,
                Measurement.date <= end_date)
            )
    session.close()
    
    precipitation = []
    
    for mDate, prcp in prcp_scores:
        precipitation_dict = {}
        precipitation_dict["Date"] = mDate
        precipitation_dict["Precipitation"] = prcp
        precipitation.append (precipitation_dict)

    return jsonify(precipitation)

@app.route("/api/v1.0/stations")
def stations():
    #Fetching a list of all stations
    
    session = Session(engine)
    results = session.query (Station.station, Station.name).all()
    session.close()
    
    all_stations = []
    
    for station, name in results:
        all_stations_dict = {}
        all_stations_dict["Station"] = station
        all_stations_dict["Name"] = name
        all_stations.append (all_stations_dict)

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    #Fetching temperature information for last 12 months
    session = Session(engine)
       
    active_stations = session.query (Measurement.station, func.count(Measurement.station).label('row_count')).\
                    group_by(Measurement.station).order_by (desc ("row_count")).all()
    most_active_station = active_stations[0][0]
    
    #Calculating start and end dates and transforming them to datetime formats
    most_recent_date_temp_str = session.query (Measurement.date).order_by(Measurement.date.desc()).first()
    end_date = dt.datetime.strptime (most_recent_date_temp_str[0], '%Y-%m-%d')
    start_date = end_date - dt.timedelta (days = 366)
    
    most_active_station_temp = session.query (Measurement.date, Measurement.tobs).\
        filter (Measurement.station == most_active_station).\
        filter (Measurement.date >= start_date).\
        filter (Measurement.date <= end_date).all()
    session.close()
    
    tobs_most_active_station = []
    
    for mDate, temperature in most_active_station_temp:
        tobs_most_active_station_dict = {}
        tobs_most_active_station_dict["Date"] = mDate
        tobs_most_active_station_dict["TOBS"] = temperature
        tobs_most_active_station.append (tobs_most_active_station_dict)

    return jsonify(tobs_most_active_station)

@app.route("/api/v1.0/<start>")
def temp_stats_startdate(start):
    #Fetching temperature stats for dates greater than or equal to Start date
    session = Session(engine)
    
    #Formatting user input to datetime formats
    start_date_formatted = dt.datetime.strptime (start, '%m-%d-%Y')
    results = session.query (func.min (Measurement.tobs), func.avg (Measurement.tobs), func.max(Measurement.tobs)).\
                    filter (Measurement.date >= start_date_formatted).all()
    session.close()

    stats = []
    
    for tmin, tavg, tmax in results:
        stats_temp = {}
        stats_temp["TMIN"] = tmin
        stats_temp["TAVG"] = tavg
        stats_temp["TMAX"] = tmax
        stats.append (stats_temp)

    if stats[0]["TMIN"] == "" or stats[0]["TMIN"] is None:
        return jsonify ({"Error": "No Record Found. Data available for dates between 01-01-2017 and 08-23-2017 (mm-dd-yyyy) only."}), 404
    
    return jsonify(stats)

@app.route("/api/v1.0/<start>/<end>")
def temp_stats_start_enddate(start, end):
    #Fetching temperature stats for dates between start date and end date
    session = Session(engine)
     
     #Formatting user input to datetime formats
    start_date_formatted = dt.datetime.strptime (start, '%m-%d-%Y')
    end_date_formatted = dt.datetime.strptime (end, '%m-%d-%Y')

    results = session.query (func.min (Measurement.tobs), func.avg (Measurement.tobs), func.max(Measurement.tobs)).\
                    filter (Measurement.date >= start_date_formatted).\
                    filter (Measurement.date <= end_date_formatted).all()
    session.close()
    
    stats = []
    
    for tmin, tavg, tmax in results:
        stats_temp = {}
        stats_temp["TMIN"] = tmin
        stats_temp["TAVG"] = tavg
        stats_temp["TMAX"] = tmax
        stats.append (stats_temp)
    
    if stats[0]["TMIN"] == "" or stats[0]["TMIN"] is None:
        return jsonify ({"Error": "No Record Found. Data available for dates between 01-01-2017 and 08-23-2017 (mm-dd-yyyy) only."}), 404
    
    return jsonify(stats)
    
if __name__ == "__main__":
    app.run(debug=True)