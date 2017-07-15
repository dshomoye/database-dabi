from flask_restful import Resource, abort, reqparse
from models import *

# from /stations 
class Stations(Resource):
    def get(self):
        return get_all_stations()

#from /schedule
class Schedule(Resource):
    def get(self):
        schedule_parser = reqparse.RequestParser()
        schedule_parser.add_argument('start_station',required=True)
        schedule_parser.add_argument('end_station',required=True)
        schedule_parser.add_argument('trip_date',required=True)
        schedule_parser.add_argument('time_of_day')
        args = schedule_parser.parse_args()
        start_station = get_station_id(args['start_station'].upper())
        end_station= get_station_id( args['end_station'].upper() )
        time_of_day = args['time_of_day']
        if not time_of_day: 
            time_of_day = "anytime"
        else:
            time_of_day=time_of_day.lower()
        trip_date=args['trip_date']
        r = get_trains_from_station(start_station,end_station,trip_date,time_of_day)
        if r :
            return r,200
        else:
            abort(404, message="invalid argument")