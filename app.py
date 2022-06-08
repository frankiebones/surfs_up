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
