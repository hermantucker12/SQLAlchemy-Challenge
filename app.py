from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

app = Flask(__name__)

hello_dict = {"Hello": "World!"}


@app.route("/")
def home():
    return '''
    <h1> Welcome to Hawaii's Climate App </h1>
    <p>Please naviate to the follow paths:</p>
    <ul>
        <li>/api/v1.0/precipitation</li>
        <li>/api/v1.0/stations</li>
        <li>/api/v1.0/tobs</li>
        <li>/api/v1.0/&lt;start&gt;</li>
        <li>/api/v1.0/&lt;start&gt;/&lt;end&gt;</li>
    </ul>
'''

# <li>/api/v1.0/<start> and /api/v1.0/<start>/<end></li>

@app.route('/api/v1.0/precipitation')
def precipitation():
    result = session.query(Measurement.date, Measurement.prcp).all()
    return { date:prcp for date, prcp in result }


@app.route('/api/v1.0/stations')
def station():
    result = session.query(Station.station,Station.name).all()
    return { id:location for id,location in result }



@app.route("/api/v1.0/tobs")
def tobs():
    most_active_stations = session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()
    station_highest_obs = most_active_stations[0][0]
    results = session.query(Measurement.date, Measurement.tobs).\
                        filter(Measurement.date >= "2016-08-23").\
                        filter(Measurement.date <= "2017-08-23").\
                        filter(Measurement.station == station_highest_obs).order_by(Measurement.date).all()
    return { date:tobs for date, tobs in results }



@app.route("/api/v1.0/<startDate>")
def Start_date(startDate):
    result = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= startDate).all()
    start_date_tobs = []
    for min, avg, max in result:
        start_date_tobs_dict = {}
        start_date_tobs_dict["min_temp"] = min
        start_date_tobs_dict["avg_temp"] = avg
        start_date_tobs_dict["max_temp"] = max
        start_date_tobs.append(start_date_tobs_dict) 
    return jsonify(start_date_tobs)



@app.route("/api/v1.0/<start_date>/<end_date>")
def Start_end_date(start_date, end_date):
    result = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    start_end_tobs = []
    for min, avg, max in result:
        start_end_tobs_dict = {}
        start_end_tobs_dict["min_temp"] = min
        start_end_tobs_dict["avg_temp"] = avg
        start_end_tobs_dict["max_temp"] = max
        start_end_tobs.append(start_end_tobs_dict) 
    return jsonify(start_end_tobs)


if __name__ == "__main__":
    app.run(debug=True)