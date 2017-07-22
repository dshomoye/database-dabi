import os,tempfile, shutil
from dabi import app
from flask import json
from dabi.models import *
import unittest


class DabiTestCase(unittest.TestCase):

    def setUp(self):
        self.db = app.config['DATABASE']
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        shutil.copy2(self.db, app.config['DATABASE'])
        self.app = app.test_client()

    
    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])
        app.config['DATABASE'] = self.db


    #test API endpoints
    def test_stations_api(self):
        r = self.app.get('/stations')
        d = json.loads(r.data)
        assert {
        "station_code": "BOST", 
        "station_name": "Boston South Station, MA"
        }  in d

    def test_schedule_api(self):
        r = self.app.get('/schedule?start_station=TRNT&end_station=BDPR&trip_date=2017-5-24&time_of_day=Morning')
        d = json.loads(r.data)
        assert {
                    u'arrival': u'07:45:00', 
                    u'fare': 14, u'time_out': 
                    u'06:02:00', u'train_num': 1
                } in d
    
    def test_passenger_api(self):
        p = self.app.get('passengers/1')
        self.assertEqual(json.loads(p.data),
            {
                "first_name": "Butt", "last_name": "Abu", 
                "email": "buttabu@yahoo.com", 
                "address": "160 Convent Ave, New York, NY 11103"
            }
            )
    def test_tickets_api(self):
        ct = self.app.post("/tickets?start_station=TRNT&end_station=BDRP&trip_date_time=2017-5-24 07:45:00&train_number=1&passenger_id=2&fare=14")
        self.assertNotEqual(ct,"null")
        d = ct.data
        ti = self.app.get('/tickets/%s'%d)
        #TODO set this to assert the right JSON is is returned
        self.assertNotEqual(ti.data,"null")

    #test some models functions
    def test_get_stations(self):
        rv = get_all_stations()
        assert    {
        "station_code": "BOST", 
        "station_name": "Boston South Station, MA"
    } in rv

    def test_get_trains(self):
        rv = get_all_trains()
        for i in range(1,28):
            assert i in rv
    
    def test_create_passenger(self):
        p = create_passenger("John","Smith","777 ysw, 2938","dsd@dsaew","js","jsp")
        pi = get_passenger_info(p)
        self.assertNotEqual(check_p_id(p),None)
        #self.assertEqual(pi,["John","Smith","777 ysw, 2938","dsd@dsaew"])
    
    def test_create_ticket(self):
        t = create_ticket(1, 1, 2, u'2017-04-10 06:55:55', 1,20)
        self.assertNotEqual(t,None)
    

if __name__ == '__main__':
    unittest.main()

    