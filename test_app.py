import pytest
from flask import Flask
from flask import redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from models import db
from models import Events, Users, TimeRanges
from dotenv import load_dotenv
import os
import datetime
import random, string
import psycopg2
import unittest
from app import app
from app import get_time


class BaseTestCase(unittest.TestCase):

    def create_app(self):
        #app = Flask(__name__, static_url_path='', static_folder='static')
        #DATABASE_URL = os.environ.get("DATABASE_URL_TEST")
        POSTGRES = {
            'user': 'when2meet',
            'pw': '1234',
            'db': 'when2meet_test',
            'host': 'localhost',
            'port': '5432',
        }
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
        app.config['DEBUG'] = True
        #app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
        #conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        db.init_app(app)
        return app

    def setUp(self):        
        with app.app_context():
            db.create_all()
            e = Events(name="First Test", timeblock=1, dateStart=datetime.date(2019,3,24), dateEnd=datetime.date(2019,3,24), token="easy10curl")
            db.session.add(e)
            u1 = Users(name="Akira", event=e)
            db.session.add(u1)            
            db.session.add(TimeRanges(user=u1, timeStart = datetime.datetime(2019,3,24,12,0,0), timeEnd = datetime.datetime(2019,3,24,17,0,0)))
            u2 = Users(name="Mugen", event=e)
            db.session.add(u2)            
            db.session.add(TimeRanges(user=u2, timeStart = datetime.datetime(2019,3,24,7,0,0), timeEnd = datetime.datetime(2019,3,24,19,0,0)))
            u3 = Users(name="Jin", event=e)
            db.session.add(u3)            
            db.session.add(TimeRanges(user=u3, timeStart = datetime.datetime(2019,3,24,11,0,0), timeEnd = datetime.datetime(2019,3,24,13,0,0)))
            u4 = Users(name="Fuu", event=e)
            db.session.add(u4)            
            db.session.add(TimeRanges(user=u4, timeStart = datetime.datetime(2019,3,24,1,0,0), timeEnd = datetime.datetime(2019,3,24,23,0,0)))              
            db.session.commit()
                           
    def tearDown(self):
        db.session.remove()
        db.drop_all()

class FlaskTestCases(BaseTestCase):
    #test to make sure if visiting broken link 404 is thrown
    def test_invalid_link(self):
        self.client.get('/events/faketoken')
        self.assert_template_used('hello.html')

    #test first event where optimal time should be 12pm-1pm
    def test_get_time(self):
        with app.test_request_context('events/easy10curl'):
            response = self.client.get.get_time("easy10curl").data
            self.assertEquals("3/24/2019 12:00 PM to 3/24/2019 1:00 PM", response)
    
    
    '''
    @pytest.fixture(scope='module')
    def new_event():
        event_name = "First Test"
        start_date = datetime.datetime.now()
        end_date = start_date
        token = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        timeblock = 1

        e = Events(name=event_name, timeblock=timeblock, dateStart=start_date, dateEnd=end_date, token=token)

        return e
 
    def test_create_event(new_event):    
        assert new_event.name == "First Test"
        assert isinstance(new_event.dateStart,datetime.datetime)


    

    @pytest.fixture(scope='module')
    def new_event2():

        event_name = "Second Test" 
        token = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        timeblock = 3
        dateS = dateStart.strftime('6/1/2019')
        dateE = dateEnd.strftime('6/3/2019')
        start_date = datetime.datetime.now()
        end_date = start_date
        e = Events(name=event_name, timeblock=timeblock, dateStart=start_date, dateEnd=end_date, token=token)

        return e

    def test_event2(new_event2):
        assert new_event2.name == "Second Test"
        assert isinstance(new_event2.dateStart,datetime.datetime)

    '''
