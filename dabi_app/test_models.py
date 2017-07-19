import os,tempfile, shutil
from app import app
from flask import json
from app.models import *
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
    

    #tests for view routes
    #TODO: need better test params!
    def test_index_page(self):
        r = self.app.get('/')
        assert b'Welcome' in r.data
    
    def test_check_schedule(self):
        r = self.app.get('/check_schedule')
        ## verify page contains a station
        assert b'Providence' in r.data

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
        assert {u'arrival': u'07:45:00', u'time_out': u'06:02:00', u'train_num': 1} in d
    

    #some tests for models functions
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
    

if __name__ == '__main__':
    unittest.main()

    