from flask import Flask
from flask import redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from models import db
from models import Events, Users, TimeRanges
from dotenv import load_dotenv
import os
import datetime
import random, string


load_dotenv()

app = Flask(__name__, static_url_path='', static_folder='static') #/static folder to hold static files by default.

DATABASE_URL = os.environ.get("DATABASE_URL")

POSTGRES = {
    'user': 'when2meet',
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

@app.route('/events/<event_token>', methods=['GET', 'POST'])
def event(event_token):
    # show the post with the given id, the id is an integer
    if request.method=='GET':
    	print('in get')
    	e = db.session.query(Events).filter(Events.token==event_token).first()
    	print(e)
    	if e is None:
    		return render_template('404.html')
    	else:
            dateS = e.dateStart.strftime('%m/%d/%Y')
            dateE = e.dateEnd.strftime('%m/%d/%Y')
            return render_template('event.html', event=e, dateS=dateS, dateE=dateE)
    if request.method=='POST':
    	print('in post')
    	e = db.session.query(Events).filter(Events.token==event_token).first()
    	print(request.form)
    	username=request.form['username']
    	print(username)
    	print(e)
    	u = Users(name=username, event=e)
    	print('printing u', u)
    	db.session.add(u)
    	start_time=request.form['start_time']
    	end_time=request.form['end_time']
    	t = TimeRanges(user=u, timeStart=start_time, timeEnd=end_time)
    	db.session.add(t)
    	db.session.commit()
    	return redirect('/')
    #return 'Post %d' % post_id

@app.route('/events/<event_token>/getTime', methods=['GET'])
def get_time(event_token):
	if request.method=='GET':
		e = db.session.query(Events).filter(Events.token==event_token)


@app.route('/create_event', methods=['GET','POST'])
def create_event():
	print('in-create')
	if request.method=='GET':
		return render_template('create.html')
	if request.method=='POST':
		print('in post')
		print(request.form)
		event_name=request.form['event_name']
		start_date=request.form['start_date']
		end_date=start_date
		timeblock=request.form['timeblock']
		#10 Digit/Char long Alphanumeric token generated randomly
		token= ''.join(random.choices(string.ascii_letters + string.digits, k=10))
		e = Events(name=event_name, timeblock=timeblock, dateStart=start_date, dateEnd=end_date, token=token)
		db.session.add(e)
		db.session.commit()
		return render_template('token.html', token=token)
