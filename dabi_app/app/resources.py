from flask_restful import Resource, abort
from models import *

# from /stations 
class Stations(Resource):
    def get(self):
        return get_all_stations()


# routed from /schedule?
class Train_schedule(Resource):
    def get(self,start_station,end_station,trip_date,time_of_day):
        start_station = get_station_id(start_station.upper())
        end_station = get_station_id(end_station.upper())
        r = get_trains_from_station(start_station,end_station,trip_date,time_of_day.lower())
        if r :
            return r,200
        else:
            abort(404, message="invalid argument")