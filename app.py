import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# create database engine
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect the database
Base = automap_base()
Base.prepare(engine, reflect=True)

# create references to both tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# create session link
session = Session(engine)

# create a Flask App instance
app = Flask(__name__)

# create the Welcome route
# root
@app.route('/')

# create the welcome function
def welcome():
    
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')
    
# create precipitaion route
@app.route("/api/v1.0/precipitation")

# create the precipitation function
def precipitation():

    # calculate date from 1 year ago
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    # query date and precipitation for previous year
    precipitation = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= prev_year).all()
    
    # create dictionary with date as key/precipitation as value
    precip = {date: prcp for date, prcp in precipitation}

   # convert dictionary to json file 
    return jsonify(precip)

# create the stations route
@app.route("/api/v1.0/stations")

# create the stations function
def stations():

    # query that retrieves all stations
    results = session.query(Station.station).all()

    # unravel results into a one-dimensional array then convert to a list
    stations = list(np.ravel(results))

    return jsonify(stations=stations)

# create the temperature observations route
@app.route("/api/v1.0/tobs")

# create the temperature observations function
def temp_monthly():

    # calculate date from 1 year ago
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # query temperature observations for primary station for previous year
    results = session.query(Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= prev_year).all()
    
    # unravel results into a one-dimensional array then convert to a list
    temps = list(np.ravel(results))

    return jsonify(temps=temps)

# create statitics starting route
@app.route("/api/v1.0/temp/<start>")

# create statistics ending route
@app.route("/api/v1.0/temp/<start>/<end>")

# create statistics function
def stats(start=None, end=None):

    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:

        results = session.query(*sel).filter(Measurement.date >= start).all()

        temps = list(np.ravel(results))

        return jsonify(temps=temps)

    results = session.query(*sel).filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    temps = list(np.ravel(results))

    return jsonify(temps=temps)