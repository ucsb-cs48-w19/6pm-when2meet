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
    dateS = e.dateStart.strftime('6/1/2019')
    dateE = e.dateEnd.strftime('6/3/2019')
    start_date = datetime.datetime.now()
    end_date = start_date
    e = Events(name=event_name, timeblock=timeblock, dateStart=start_date, dateEnd=end_date, token=token)
    
    
    #return render_template('event.html', event=e, dateS=dateS, dateE=dateE)
    return e
   
def test_event2(new_event2):
    assert new_event2.name == "Second Test"
    assert isinstance(new_event2.dateStart,datetime.datetime)
