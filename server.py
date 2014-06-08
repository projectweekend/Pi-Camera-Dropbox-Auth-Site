import os
from dropbox.client import DropboxOAuth2Flow
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


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/whoops')
def whoops():
    return render_template('whoops.html')


@app.route('/sorry')
def sorry():
    return render_template('sorry.html')


@app.route('/token')
def token():
    flow = DropboxOAuth2Flow(DROPBOX_KEY, DROPBOX_SECRET, REDIRECT_URI,
                                session, 'dropbox-auth-csrf-token')
    try:
        access_token, user_id, url_state = flow.finish(request.args)
    except DropboxOAuth2Flow.BadStateException:
        return redirect('/')
    except (DropboxOAuth2Flow.BadRequestException,
            DropboxOAuth2Flow.CsrfException,
            DropboxOAuth2Flow.ProviderException):
        return redirect('/whoops')
    except DropboxOAuth2Flow.NotApprovedException:
        return redirect('/sorry')
    response = make_response(access_token)
    response.headers['Content-Disposition'] = 'attachment; filename=dropbox.txt'
    return response
