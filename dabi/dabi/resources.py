from flask_restful import Resource, abort, reqparse
from models import *
from . import pwd_context
import datetime
import jwt


def check_token(token,hashp):
    if not Token:
        return False
    try:
        d = jwt.decode(token,hashp)
    except:
        return False
    return True

# from /stations 
class Stations(Resource):
    def get(self):
        return get_all_stations()

class Token(Resource):
    def post(self):
        sp = reqparse.RequestParser()
        sp.add_argument("username",required=True)
        sp.add_argument("password",required=True)
        args = sp.parse_args()

        pauth = get_user_auth(args["username"])
        
        if pwd_context.verify(args["password"], pauth):
            token = jwt.encode({"username":args["username"],
                 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
            },
            pauth
            )
            return {"token":token}
        return "Login failed, verify username and password",403


class Passenger(Resource):
    def get(self,passenger_id):
        hashp = get_passenger_auth(passenger_id)
        sp = reqparse.RequestParser()
        sp.add_argument("token", required=True)
        args = sp.parse_args()

        if not check_token(args["token"],hashp):
            return "Invalid token",403

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
    
    def post(self):
        sp = reqparse.RequestParser()
        sp.add_argument("first_name",required=True)
        sp.add_argument("last_name",required=True)
        sp.add_argument("email",required=True)
        sp.add_argument("address")
        sp.add_argument("username",required=True)
        sp.add_argument("password",required=True)
        args = sp.parse_args()

        if "address" not in args:
            args["address"] = None
        
        hashp = pwd_context.hash(args["password"])
        p = create_passenger(
            lname = args['last_name'],
            fname = args['first_name'],
            address = args['address'],
            email = args['email'],
            username = args["username"],
            hashp = hashp
        )
        return p

class Ticket(Resource):
    #TODO write the delete method for cancelling reservations
    #TODO write update method for rebooking cancelled trip
    def delete(self,ticket_number):
        sp = reqparse.RequestParser()
        sp.add_argument("token",required=True,help="Go to /login to retrieve a valid token")
        sp.add_argument("passenger_id",required=True,type=int)
        args = sp.parse_args()
        if not check_token(args["token"],get_passenger_auth(args["passenger_id"])):
          return "Invalid token", 403
        cancel_ticket(ticket_number)
        return "Success",200  

    def post(self):
        sp = reqparse.RequestParser()
        arguments = ["passenger_id","start_station","end_station",
                    "train_number","trip_date_time","fare"]
        for a in arguments:
            sp.add_argument(a,required=True)
        sp.add_argument("return_date_time")
        sp.add_argument("return_train")
        sp.add_argument("token")


        args = sp.parse_args()

        if not check_token(args["token"], 
        get_passenger_auth(args["passenger_id"])):
            return "Invalid token", 403

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
        return {"ticket_number": t}
    
    def get(self,ticket_number=None):
        #get info for single ticket
        if(ticket_number):
            sp = reqparse.RequestParser()
            sp.add_argument("token",required=True)
            args = sp.parse_args()
            ti = get_ticket_record(ticket_number)
            result = dict(
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
            if not check_token(args["token"], 
                        get_passenger_auth(result["passenger_id"])):
                return "Invalid token", 403
        # or get all tickets for a single passenger
        else:
            sp = reqparse.RequestParser()
            sp.add_argument("token",required=True)
            sp.add_argument("passenger_id",required=True,type=int)
            args = sp.parse_args()
            if not check_token(args["token"],get_passenger_auth(args["passenger_id"])):
                return "Invalid token", 403
            re = get_passenger_reservation(args["passenger_id"])
            result=[]
            for r in re:
                result.append(dict(
                    ticket_number = r[0],
                    train = r[1],
                    start_station = r[2],
                    end_station= r[3],
                    date = r[4],
                    round_trip = r[5],
                    return_train = r[6],
                    return_date = r[7]
                ))
            
        return result

            
            

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