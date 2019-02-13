from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class Events(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)
    timeblock = db.Column(db.Integer, nullable = False)
    dateStart = db.Column(db.DateTime, nullable = False)
    dateEnd = db.Column(db.DateTime, nullable = False)
    token = db.Column(db.String, nullable = False, unique=True)

    def __repr__(self):
        return '<Event {}>'.format(self.id)

class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    
    name = db.Column(db.String, nullable = False)

    event_id = db.Column(db.Integer, db.ForeignKey('events.id'),
        nullable=False)
    event = db.relationship('Events',
        backref=db.backref('users', lazy=True))

    def __repr__(self):
        return '<User {}>'.format(self.id)

class TimeRanges(db.Model):
    __tablename__ = 'timeranges'
    id = db.Column(db.Integer, primary_key = True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),
        nullable=False)
    user = db.relationship('Users',
        backref=db.backref('timeranges', lazy=True))

    timeStart = db.Column(db.DateTime, nullable = False) 
    timeEnd = db.Column(db.DateTime, nullable = False)

    def __repr__(self):
        return '<TimeRange {}>'.format(self.id)
