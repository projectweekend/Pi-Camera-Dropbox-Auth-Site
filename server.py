import os
from dropbox.client import DropboxOAuth2Flow, DropboxClient, ErrorResponse
from flask import Flask
from flask import session
from flask import request
from flask import redirect
from flask import make_response
from flask import render_template


app = Flask(__name__)
app.secret_key = os.environ['SESSION_KEY']
app.config['DEBUG'] = True


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

    return render_template('index.html', **template_data)


@app.route('/token')
def token():
    flow = DropboxOAuth2Flow(DROPBOX_KEY, DROPBOX_SECRET, REDIRECT_URI,
                                session, 'dropbox-auth-csrf-token')
    try:
        access_token, user_id, url_state = flow.finish(request.args)
    except ErrorResponse:
        return redirect('/')
    response = make_response(access_token)
    response.headers['Content-Disposition'] = 'attachment; filename=dropbox.txt'
    return response
