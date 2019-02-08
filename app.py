from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__, static_url_path='') #/static folder to hold static files by default.

DATABASE_URL = os.environ.get("DATABASE_URL")

POSTGRES = {
    'user': 'when2meet',
    'pw': '1234',
    'db': 'when2meet_dev',
    'host': 'localhost',
    'port': '5432',
}

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL % POSTGRES

db = SQLAlchemy()

#define models here

class User(db.Model):
    __tablename__ = "events"
    id = db.Column(db.Integer, primary_key=True)
    timeblock = db.Column(db.Integer(), nullable=False)
    event_id = db.Column(db.Integer(), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.id

db.init_app(app)

@app.route("/")
def index():
    return render_template('index.html')