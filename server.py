import os
from dropbox.client import DropboxOAuth2Flow, DropboxClient
from flask import Flask
from flask import session
from flask import render_template


app = Flask(__name__)


DROPBOX_KEY = os.environ['DROPBOX_KEY']
DROPBOX_SECRET = os.environ['DROPBOX_SECRET']
REDIRECT_URI = os.environ['REDIRECT_URI']


@app.route('/')
def index():
    flow = DropboxOAuth2Flow(DROPBOX_KEY, DROPBOX_SECRET, REDIRECT_URI,
                                session, 'dropbox-auth-csrf-token')
    template_data = {
        'authorize_url': flow.start()
    }
    return render_template('index.html', template_data)


@app.route('/token')
def function():
    return render_template('token.html')
