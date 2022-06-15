from flask import Blueprint, render_template, Flask, jsonify, request
import datetime
import pprint
import jwt
import hashlib
from flask import Request
from functools import wraps
#import db
# I need to change the password on my luggage
SECRET_KEY="12345"
import string
import random
# TODO: Figure out how to grab these from config
SUCCESS_STR = "SUCCESS"
FAIL_STR = "FAILURE"
STATUS_KEY = "STATUS"
ERROR_KEY = "ERROR"

# 5 Minute Token timeout
# TODO: Make thie configurable, so "remember me" will make a much MUCH longer token
def encode_auth_token(user_id):
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=120),
        'iat': datetime.datetime.utcnow(),
        'sub': user_id
    }
    jwtretval = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm='HS256'
    )
    try:
        jwtretval = jwtretval.decode('utf-8')
    except (UnicodeDecodeError, AttributeError):
        pass
    return jwtretval



# Be sure to return 4, I rolled 3d8 to get that.
def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    #print("Random string of length", length, "is:", result_str)
    return result_str

def decode_auth_token(auth_token,key):
    payload = jwt.decode(auth_token, key,algorithms=['HS256'])
    return payload['sub']




# Pulls the auth token out of a request if it exists in the Authorization header
def getAuthToken(request):
    auth_header = request.headers.get('Authorization')
    auth_token = ''
    if auth_header:
        try:
            auth_token = auth_header.split(" ")[1]
            return auth_token
        except:
            pass
    return None




def getJwt(request: Request):
    """Get JSON Web Token from a Flask Request Object.
    Args:
        request (Request): Request from Flask
    Returns:
        Object: The JWT object on success, None otherwise.
    """
    auth_token = getAuthToken(request)
    #pprint.pprint(auth_token)
    if auth_token:
        try:
            resp = decode_auth_token(auth_token,SECRET_KEY)
            #pprint.pprint(resp)
            #print("Cookies")
            #pprint.pprint(request.cookies)
            if resp:
                if 'mspysid' in request.cookies:
                    session = request.cookies['mspysid']
                    m = hashlib.sha256()
                    if session is not None:
                        m.update(session.encode('utf-8'))
                        if m.hexdigest() != resp['session']:
                            print('Invalid hex')
                            pprint.pprint(resp)
                            pprint.pprint(session)
                            pprint.pprint(m.hexdigest())
                            return None
                    else:
                        print('No session var')
                        return None
                    return resp
        except Exception as ex:
            print('Exception')
            print(str(ex))
            return None
    return None


roles = {
    'admin' : {
        'parent':'member3'
    },
    'member3' : {
        'parent':'member2'
    },
    'member' : {
        'parent':'guest'
    },
    'member2' : {
        'parent':'member'
    },
    'guest' : {

    }
}
role_routes = {
    '/auth' : {
        'role_required': None
    },
    '/private' : {
        'role_required':'member'
    }
}



# Wrapper function for needing jwt
# This checks the JWT expiration, as well as making sure that there is a 
# cookie (should check httponly and secure) matching the sha256 of the session ID
# Is this a good way to prevent XSS? Someone would have to hijack both the JWT, as well
# as the session cookie, which if the latter is stored in httponly, that should be impossible?
# We should invalidate tokens used with either no session, or an invalid session as an
# additional security measure.
 
def jwt_private(func):
    def wrapper_jwt_private(*args, **kwargs):
        #print('Path:')
        #pprint.pprint(request.path)
        #print("Done",flush=True)
        auth_token = getAuthToken(request)
        jwt = getJwt(request)
        if jwt is None:
            return jsonify({STATUS_KEY:FAIL_STR,ERROR_KEY:'Null session'}),401
        #pprint.pprint(jwt)
        if request.path in role_routes:
            if 'role_required' in role_routes[request.path]:
                minrole = role_routes[request.path]['role_required']
                foundrole = False
                for role in jwt['roles']:
                    if checkRole(role,minrole):
                        foundrole = True
                        break
                if foundrole:
                    return func(*args, **kwargs)
                else:
                    return jsonify({STATUS_KEY:FAIL_STR,ERROR_KEY:'Invalid permissions'}),401
        else:
            return func(*args,**kwargs)
    wrapper_jwt_private.__name__ = func.__name__
    return wrapper_jwt_private
    

def requires_access_level(access_level):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            auth_token = getAuthToken(request)
            jwt = getJwt(request)
            if jwt is None:
                return jsonify({STATUS_KEY:FAIL_STR,ERROR_KEY:'Null session'}),401
            #dbsession = db.AppSession()
            groups = jwt['user']['groups']
            print("requires_access_level: ")
            pprint.pprint(access_level)
            pprint.pprint(jwt)
            found = False
            if not jwt['user']['siteadmin']:
                for group in groups:
                    for perm in group['permissions']:
                        if perm['name'] in access_level:
                            found = True
                            break
                if not found:
                    return jsonify({STATUS_KEY:FAIL_STR,ERROR_KEY:'Permission Denied'}),403
#            pprint.pprint(perms)
            #requser = dbsession.query(User).filter(User.id == uid).first()
            #if not session.get('email'):
            #    return redirect(url_for('users.login'))
#
#            user = User.find_by_email(session['email'])
#            elif not user.allowed(access_level):
#                return redirect(url_for('users.profile', message="You do not have access to that page. Sorry!"))
            return f(*args, **kwargs)
        return decorated_function
    return decorator