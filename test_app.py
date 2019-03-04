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


class BaseTestCase(unittest.TestCase):

    def create_app(self):
        #app = Flask(__name__, static_url_path='', static_folder='static')
        DATABASE_URL = os.environ.get("DATABASE_URL")
        app.config['DEBUG'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:' #'postgresql://%(when2meet)s:\
       # %(1234)s@%(localhost)s:%(5432)s/%(when2meet_dev)s' % POSTGRES
        if DATABASE_URL is not None:
            app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        db.init_app(app)
        return app

    def setUp(self):        
        with app.app_context():
            db.create_all()
            e = Events(name="First Test", timeblock=1, dateStart=date(2019,3,24), dateEnd=date(2019,3,24), token=''.join(random.choices(string.ascii_letters + string.digits, k=10)))
            db.session.add(e)
            u = Users(name="Akira", event=e)
            db.session.add(u)            
            db.session.add(TimeRanges(user=u, timeStart = date(2019,3,24), timeEnd = date(2019,3,24))
            u = Users(name="Mugen", event=e)
            db.session.add(u)            
            db.session.add(TimeRanges(user=u, timeStart = date(2019,3,24), timeEnd = date(2019,3,24))
            u = Users(name="Jin", event=e)
            db.session.add(u)            
            db.session.add(TimeRanges(user=u, timeStart = date(2019,3,24), timeEnd = date(2019,3,24))
            u = Users(name="Fuu", event=e)
            db.session.add(u)            
            db.session.add(TimeRanges(user=u, timeStart = date(2019,3,24), timeEnd = date(2019,3,24))              
            db.session.commit()
                           
   def tearDown(self):
        db.session.remove()
        db.drop_all()

class FlaskTestCases(BaseTestCase):
    
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
    '''
    
    def test_invalid_link(self):
        e = db.session.query(Events).filter(Events.token=="faketoken").first()
        self.assertNotEqual(e, none)



    
'''
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
