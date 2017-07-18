import os,tempfile, shutil
from app import app
from app.models import *
import unittest


class ModelsTestCase(unittest.TestCase):

    def setUp(self):
        self.db = app.config['DATABASE']
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        shutil.copy2(self.db, app.config['DATABASE'])
        self.app = app.test_client()

    
    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])
        app.config['DATABASE'] = self.db
    
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

    