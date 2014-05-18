import os
import dropbox
from flask import Flask
from flask import render_template


app = Flask(__name__)

DROPBOX_KEY = os.getenv('DROPBOX_KEY')
DROPBOX_SECRET = os.getenv('DROPBOX_SECRET')



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/token')
def function():
    return render_template('token.html')
