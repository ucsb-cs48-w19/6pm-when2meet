
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

DATABASE_DEFAULT = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES


app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
if DATABASE_URL is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')

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


def overLap(tList):


    masterSet=[]
    userSets=[]

    for userTimes in tList:
        ts= userTimes[0]
        tf=userTimes[1]
        #print(ts,tf)
        tsMin = ts.hour*60+ts.minute
        tfMin = tf.hour*60+ts.minute
        print(tsMin,tfMin)
        us= set()
        us.add(range(tsMin,tsMin+1))

    print
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
    	db.session.commit()
    	return redirect(url_for('user', event_token=event_token, user_id=str(u.id))) # return render_template('userpage.html', event=e, user=u, token=event_token)
    #return 'Post %d' % post_id

@app.route('/events/<event_token>/<user_id>', methods=['GET', 'POST'])
def user(event_token, user_id):
    e = db.session.query(Events).filter(Events.token==event_token).first()
    if e is None:
        return render_template('404.html')
    u = db.session.query(Users).filter(Users.id==user_id).first()
    if request.method=='GET':
        return render_template('userpage.html', event=e, user=u, token=event_token)
    if request.method == 'POST':
        start_time=request.form['start_time']
        end_time=request.form['end_time']
        t=TimeRanges(user=u, timeStart=start_time, timeEnd=end_time)
        db.session.add(t)
        db.session.commit()
        return redirect(url_for('user', event_token=event_token, user_id=str(u.id)))

@app.route('/events/<event_token>/getTime', methods=['GET'])
def get_time(event_token):
    # show the post with the given id, the id is an integer
    if request.method=='GET':
    	e = db.session.query(Events).filter(Events.token==event_token).first()
    	if e is None:
    		return render_template('404.html')
    	else:
            #print("GETING THE FUCKIGN TIME")
            users = db.session.query(Users).filter(Users.event==e).all()
            #print(users)
            timeList=[]
            for u in users:
                uid=u.id
                t=(db.session.query(TimeRanges).filter(TimeRanges.user_id==uid).all())
                for time in t:
                    userTimes=(time.timeStart,time.timeEnd)
                    timeList.append(userTimes)
            if not timeList:
                return render_template('getTime.html',data="not avalible because nobody has input times yet",ename=e.name)

            #print("timeList",*timeList,sep='\n')
            overLap(timeList)
            bestRange="default"
            return render_template('getTime.html',data=bestRange,ename=e.name)


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
		timeblock=int(request.form['timeblock_hours'])*60+int(request.form['timeblock_min'])
		#10 Digit/Char long Alphanumeric token generated randomly
		token= ''.join(random.choices(string.ascii_letters + string.digits, k=10))
		e = Events(name=event_name, timeblock=timeblock, dateStart=start_date, dateEnd=end_date, token=token)
		db.session.add(e)
		db.session.commit()
		return render_template('token.html', token=token)
