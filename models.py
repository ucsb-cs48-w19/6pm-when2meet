from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "events"
    id = db.Column(db.Integer, primary_key=True)
    timeblock = db.Column(db.Integer(120), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.id