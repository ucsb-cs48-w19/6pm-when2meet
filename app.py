from flask import Flask
from flask import render_template
from models import db
import os


app = Flask(__name__)

POSTGRES = {
    'user': 'when2meet',
    'pw': '1234',
    'db': 'when2meet_dev',
    'host': 'localhost',
    'port': '5432',
}
@app.route("/")
def index():
    return render_template('index.html')