"""
The flask application package.
"""
import os
#import psycopg2
from datetime import datetime
from flask import render_template, Flask
#from cse412 import app

app = Flask(__name__)

#def connectDB():
    #conn = psycopg2.connect()

@app.route('/')
def home():
    """Renders the home page."""
    return render_template(
        'layout.html',
        title='Music Library System',
        year=datetime.now().year,
    )