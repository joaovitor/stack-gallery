from stack import app

from flask import redirect, url_for, session
from flask import request, abort
from functools import wraps
from httplib2 import Http
import json
import jwt
from datetime import datetime, timedelta

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        access_token = session.get('access_token')
        if access_token is None:
          print ('==> not logged. Redirect to the signin page')
          # use for How To: Redirect back to current page after sign in, sign out, sign up
          # redirect(url_for('signin', next=request.url))
          return redirect(url_for('signin'))
        return f(*args, **kwargs)
    return decorated_function

def login_authorized(fn):
    """Decorator that checks that requests
    contain an id-token in the session or request header.
    userid will be None if the
    authentication failed, and have an id otherwise.

    Usage:
    @app.route("/")
    @auth.login_authorized
    def secured_call(userid=None):
        pass
    """
    @wraps(fn)
    def decorated_function(*args, **kwargs):
        authorization = parser_webtoken_token()

        print ('login_authorized token ==> %s' % authorization )

        if not authorization: 
            # Unauthorized
            abort(401)
            return None


        user = validate_token(authorization)
        if user is None:
            print("Check returned FAIL!")
            # Unauthorized
            abort(401)
            return None
        return fn(user=user, *args, **kwargs)
    return decorated_function    


def revoke_token(access_token):
    h = Http()
    print ('revoking %s' % access_token)
    resp, cont = h.request('https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token,
                           headers={'Host': 'www.googleapis.com',
                                    'Authorization': access_token})

    print cont

    return resp


def parser_webtoken_token():
    if 'Authorization' in request.headers:
        print ('parse_token')
        jweb_token = parse_token(request)
        print (jweb_token)
        access_token =  jweb_token['sub']

        if access_token:
            oauth_token = 'OAuth %s' % access_token
            return oauth_token

    return None


def create_token(user):
    payload = {
        'sub': user.id,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(days=14)
    }
    token = jwt.encode(payload, app.config['SECRET_KEY'])
    return token.decode('unicode_escape')  


def parse_token(req):
    token = req.headers.get('Authorization').split()[1]
    return jwt.decode(token, app.config['SECRET_KEY'])



# def get_oauth_token():
#     access_token = session.get('access_token')
#     if access_token:
#         oauth_token = 'OAuth %s' % access_token[0]
#         return oauth_token
#     else:
#         if 'Authorization' in request.headers:
#             return request.headers['Authorization']
#         else:   
#             return None

# put this in for example gauth.py
# ref: http://flask.pocoo.org/snippets/125/
def validate_token(access_token):
    '''Verifies that an access-token is valid and
    meant for this app.

    Returns None on fail, and an User on success'''
    h = Http()
    resp, cont = h.request("https://www.googleapis.com/oauth2/v2/userinfo",
                           headers={'Host': 'www.googleapis.com',
                                    'Authorization': access_token})

    if not resp['status'] == '200':
        return None

    try:
        data = json.loads(cont)
    except TypeError:
        # Running this in Python3
        # httplib2 returns byte objects
        data = json.loads(cont.decode())

    data['oauth_token'] = access_token

    return data