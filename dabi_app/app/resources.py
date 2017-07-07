from flask_restful import Resource
from models import *

class Stations(Resource):
    def get(self):
        return get_all_stations()

class Train_schedule(Resource):
    def get(self,start_station,end_station,trip_date,time_of_day):
        start_station = get_station_id(start_station)
        end_station = get_station_id(end_station) 
        return get_trains_from_station(start_station,end_station,trip_date,time_of_day), 200