from flask_restful import Resource, abort, reqparse
from models import *

# from /stations 
class Stations(Resource):
    def get(self):
        return get_all_stations()

class Passenger(Resource):
    def get(self,passenger_id):
        p = get_passenger_info(passenger_id)
        if p:
            p = dict(
                first_name = p[1],
                last_name = p[2],
                address = p[3],
                email = p[4]
            )
            return p
        return None

class Ticket(Resource):
    def post(self):
        sp = reqparse.RequestParser()
        arguments = ["passenger_id","start_station","end_station",
                    "train_number","trip_date_time","fare"]
        for a in arguments:
            sp.add_argument(a,required=True)
        sp.add_argument("return_date_time")
        sp.add_argument("return_train")

        args = sp.parse_args()
        if(args["return_date_time"] and args["return_train"]):
            round_trip = 1
            return_date_time = args["return_date_time"]
            return_train = args["return_train"]
        else:
            round_trip = 0
            return_date_time = None
            return_train = None
        t = create_ticket(
                passenger_id = args["passenger_id"],
                start_station = args["start_station"],
                end_station = args["end_station"],
                train_num = args["train_number"],
                trip_date_time = args["trip_date_time"],
                fare = args["fare"],
                round_trip = round_trip,
                return_date_time = return_date_time,
                return_train = return_train
        )
        #the ticket number or None if failed
        return t
    
    def get(self,ticket_number):
        ti = get_ticket_record(ticket_number)
        return dict(
            start_station = ti[1],
            end_station = ti[2],
            train_number = ti[3],
            trip_date_time = ti[4],
            passenger_id = ti[5],
            round_trip = ti[6],
            return_train = ti[7],
            return_date_time = ti[8],
            fare=ti[9]
        )

            
            

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
            abort(404)