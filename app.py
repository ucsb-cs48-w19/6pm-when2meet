from flask import Flask
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy
from models import db
from dotenv import load_dotenv
import os
import datetime

load_dotenv()

app = Flask(__name__, static_url_path='') #/static folder to hold static files by default.

DATABASE_URL = os.environ.get("DATABASE_URL")

POSTGRES = {
    'user': 'postgres',
    'pw': '1234',
    'db': 'when2meet_dev',
    'host': 'localhost',
    'port': '5432',
}

app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
if DATABASE_URL is not None:
	app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
	

db.init_app(app)

print('sql config: ', app.config['SQLALCHEMY_DATABASE_URI'])
# print('DATABASE_URL: ', DATABASE_URL)
# print('POSTGRES: ', POSTGRES)

# test
# def testCreateEvent():
# 	tb = 2
# 	ds = datetime.datetime.now()
# 	de = datetime.datetime.now()
# 	t = 'ABCD'
# 	e = Events(timeblock = tb, dateStart = ds, dateEnd = de, token = t) 


@app.route("/")
def index():
    return render_template('index.html')

@app.route('/<event_token>', methods=['GET', 'POST'])
def event(event_token):
    # show the post with the given id, the id is an integer
    if request.method=='GET':
    	e = db.session.query(Events).filter(Events.token==event_token)
    	if e is None:
    		return ('404.html')
    	return ('event.html')
    if request.method=='POST':
    	e = db.session.query(Events).filter(Events.token==event_token)
    	username=request.form['username']
    	u = Users(name=username, event=e[0])
    	db.session.add(u)
    	start_time=request.form['start_time']
    	end_time=request.form['end_time']
    	t = TimeRanges(user=u, timeStart=start_time, timeEnd=end_time)
    	db.session.add(t)
    	db.session.commit()
    	return ('event.html')
    #return 'Post %d' % post_id

@app.route('/<event_token>/getTime', methods=['GET'])
def get_time(event_token):
	if request.method=='GET':
		e = db.session.query(Events).filter(Events.token==event_token)


@app.route('/create_event', methods=['POST'])
def create_event():
	if request.method=='GET':
		event_name=request.form['event_name']
		start_date=request.form['start_date']
		end_date=request.form['end_date']
		timeblock=request.form['time_block']
		token='ABCD' 
		e = Events(name=event_name, timeblock=timeblock, dateStart=start_date, dateEnd=end_date, token=token)
		db.session.add(e)
		db.session.commit()
		return render_template('index.html', token)



	



