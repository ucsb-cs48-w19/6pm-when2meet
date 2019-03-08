
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
import math

# for local .env imports
load_dotenv()

app = Flask(__name__, static_url_path='', static_folder='static') #/static folder to hold static files by default.

# if env db url exists (i.e. heroku)
DATABASE_URL = os.environ.get("DATABASE_URL")


# setting up default db user (for local use)
POSTGRES = {
	'user': 'when2meet',
	'pw': '1234',
	'db': 'when2meet_dev',
	'host': 'localhost',
	'port': '5432',
}

DATABASE_DEFAULT = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
if DATABASE_URL is not None:
	app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
	conn = psycopg2.connect(DATABASE_URL, sslmode='require')

db.init_app(app)


# route for returning index page
@app.route("/")
def index():
	return render_template('index.html')

# route for returning event page for users to create users
@app.route('/events/<event_token>', methods=['GET', 'POST'])
def event(event_token):
	# show the post with the given id, the id is an integer
	if request.method=='GET':
		e = db.session.query(Events).filter(Events.token==event_token).first()
		if e is None:
			return render_template('404.html')
		else:
			dateS = e.dateStart.strftime('%m/%d/%Y')
			dateE = e.dateEnd.strftime('%m/%d/%Y')
			users = db.session.query(Users).filter(Users.event_id==e.id).all()
			return render_template('event.html', event=e, users=users, dateS=dateS, dateE=dateE)
	if request.method=='POST':
		e = db.session.query(Events).filter(Events.token==event_token).first()
		username=request.form['username']
		u = Users(name=username, event=e)
		db.session.add(u)
		db.session.commit()
		return redirect(url_for('user', event_token=event_token, user_id=str(u.id), submission_success=False))

# route for returning user page
@app.route('/events/<event_token>/<user_id>', methods=['GET', 'POST'])
def user(event_token, user_id):
	e = db.session.query(Events).filter(Events.token==event_token).first()
	if e is None:
		return render_template('404.html')
	u = db.session.query(Users).filter(Users.id==user_id).first()
	if request.method=='GET':
		submission_success = False
		if request.args.get('submission_success'):
			submission_success = request.args.get('submission_success')
		return render_template('userpage.html', event=e, user=u, token=event_token, submission_success=submission_success)
	if request.method == 'POST':
		start_time=request.form['start_time']
		end_time=request.form['end_time']
		t=TimeRanges(user=u, timeStart=start_time, timeEnd=end_time)
		db.session.add(t)
		db.session.commit()
		return redirect(url_for('user', event_token=event_token, user_id=str(u.id), submission_success=True))

# route for returning user personalized edit page
@app.route('/events/<event_token>/<user_id>/edit', methods=['GET', 'POST'])
def user_edit(event_token, user_id):
	e = db.session.query(Events).filter(Events.token==event_token).first()
	if e is None:
		return render_template('404.html')
	u = db.session.query(Users).filter(Users.id==user_id).first()
	if request.method=='GET':
		t = db.session.query(TimeRanges).filter(u.id==TimeRanges.user_id).all()
		return render_template('useredit.html', event=e, user=u, times=t)

# route for deleting time post method
@app.route('/deleteTime/<time_id>', methods=['POST'])
def delete_time(time_id):
	t = db.session.query(TimeRanges).filter(TimeRanges.id==time_id).first()
	if t is None:
		return render_template('404.html')
	u = db.session.query(Users).filter(Users.id == t.user_id).first()
	e = db.session.query(Events).filter(Events.id == u.event_id).first()
	if request.method == 'POST':
		db.session.delete(t)
		db.session.commit()
		return redirect(url_for('user_edit', event_token=e.token, user_id=str(u.id)))

# func: converting time in minutes to nice stringified format
def intToTime(t,e):
	eStartDate=e.dateStart
	eEndDate=e.dateEnd
	minYear = eStartDate.year
	minMonth = eStartDate.month
	minDay = eStartDate.day

	timeTag=""
	time=""
	y = math.trunc(t/525600)
	t=t-y*525600
	m=math.trunc(t/43800)
	t=t-m*43800
	d=math.trunc(t/1440)
	t=t-d*1440

	year=y+minYear
	month = m+minMonth
	day=d+minDay

	if t <60:
		if t %60 <10:
			return "12:0"+str(t) + " AM"
		else:
			return "12:"+str(t) + " AM"
	if t <12*60:
		timeTag=" AM"
		if t %60 <10:
			time = str(month)+"/"+str(day)+"/"+str(year)+" "+str(math.trunc(t/60))+":0"+str(t % 60)+timeTag
		else:
			time = str(month)+"/"+str(day)+"/"+str(year)+" "+str(math.trunc(t/60))+":"+str(t % 60)+timeTag

	if t>=12*60:
		timeTag=" PM"
		if t %60 <10:
			time = str(month)+"/"+str(day)+"/"+str(year)+" "+str(math.trunc(t/60)-12)+":0"+str(t % 60)+timeTag
		else:
			time = str(month)+"/"+str(day)+"/"+str(year)+" "+str(math.trunc(t/60)-12)+":"+str(t % 60)+timeTag

	if t>=12*60 and t<13*60:
		timeTag=" PM"
		if t %60 <10:
			time = str(month)+"/"+str(day)+"/"+str(year)+" "+str(math.trunc(t/60))+":0"+str(t % 60)+timeTag
		else:
			time = str(month)+"/"+str(day)+"/"+str(year)+" "+str(math.trunc(t/60))+":"+str(t % 60)+timeTag



	return str(time)


# func: calculates overlaps over times given list of user times (assuming each element tList is a user's list of times)
def overLap(tList,e):
	masterSet=[]
	userSets=[]


	eStartDate=e.dateStart
	eEndDate=e.dateEnd

	minYear = eStartDate.year
	minMonth = eStartDate.month
	minDay = eStartDate.day

	for i in range(len(tList)):
		tset=set()
		for tr in tList[i]:
			st = tr[0]
			et = tr[1]
			smin = (st.year-minYear)*525600+(st.month-minMonth)*43800+(st.day-minDay)*1440+st.hour*60+st.minute
			emin = (et.year-minYear)*525600+(et.month-minMonth)*43800+(et.day-minDay)*1440+et.hour*60+et.minute
			for i in range(smin,emin+1):
				tset.add(i)

		userSets.append(tset)

	masterSet=userSets[0]
	for i in range (1,len(tList)):

		masterSet=masterSet.intersection(userSets[i])


	masterList= list(masterSet)
	masterList.sort()

	returnList=[]
	prev=0

	for i in range (len(masterList)):
		if i != len(masterList)-1 and masterList[i] != (masterList[i+1]-1):
			t=masterList[prev:i+1]
			prev=i+1
			returnList.append(t)
		if i == len(masterList)-1:
			t=masterList[prev:i+1]
			returnList.append(t)
	cleanRetList=[]
	for l in returnList:
		tup = (min(l),max(l))
		cleanRetList.append(tup)

	return cleanRetList

# route for returning optimal time to meet
@app.route('/events/<event_token>/getTime', methods=['GET'])
def get_time(event_token):
	# show the post with the given id, the id is an integer
	if request.method=='GET':
		e = db.session.query(Events).filter(Events.token==event_token).first()
		if e is None:
			return render_template('404.html')
		else:
			users = db.session.query(Users).filter(Users.event_id==e.id).all()
			users = db.session.query(Users).filter(Users.event==e).all()
			timeList=[]
			for u in users:
				uid=u.id
				t=(db.session.query(TimeRanges).filter(TimeRanges.user_id==uid).all())
				userTimes=[]
				for time in t:
					userTimes.append((time.timeStart,time.timeEnd))
				timeList.append(userTimes)

			if not timeList:
				return render_template('getTime.html',data="not available because nobody has input times yet",ename=e.name, users=users)

			overlap=overLap(timeList,e)
			if not overlap:
				return render_template('getTime.html',data="not available, because there were no overlapping times",ename=e.name, users=users)

			for r in overlap:
				if r[1]-r[0]<e.timeblock:
					overlap.remove(r)

			if not overlap:
				return render_template('getTime.html',data="not available, because none of the time ranges were long enough",ename=e.name, users=users)


			for i in range(len(overlap)):
				r=overlap[i]
				if r[1]-r[0]>e.timeblock:
					overlap[i]=((r[0],r[0]+e.timeblock))

			bestRange=""
			for i in range(len(overlap)):
				r=overlap[i]
				if i != len(overlap)-1:
					bestRange= bestRange +" "+intToTime(r[0],e)+" to "+intToTime(r[1],e) + " and "
				else:
					bestRange= bestRange +" "+intToTime(r[0],e)+" to "+intToTime(r[1],e)


			return render_template('getTime.html',data=bestRange,ename=e.name, users=users)

# route for creating an event
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
		end_date=request.form['end_date']
		#end_date=start_date
		timeblock=int(request.form['timeblock_hours'])*60+int(request.form['timeblock_min'])
		#10 Digit/Char long Alphanumeric token generated randomly
		token= ''.join(random.choices(string.ascii_letters + string.digits, k=10))
		e = Events(name=event_name, timeblock=timeblock, dateStart=start_date, dateEnd=end_date, token=token)
		db.session.add(e)
		db.session.commit()
		return render_template('token.html', token=token)
