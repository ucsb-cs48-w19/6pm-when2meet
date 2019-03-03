import pytest

import random
import datetime
 
 
@pytest.fixture(scope='module')
def new_event():
    event_name = "First Test"
    start_date = datetime.datetime.now()
    end_date = start_date
    ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    timeblock = 1
    
    e = Events(name=event_name, timeblock=timeblock, dateStart=start_date, dateEnd=end_date, token=token)
    
    return e

def test_create_event(new_event):
    
    
    assert e.name == "First Test"
    assert isinstance(e.dateStart,datetime.datetime)
