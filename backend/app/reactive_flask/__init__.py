from flask import Blueprint, render_template, Flask, jsonify, request
import datetime
import pprint
import jwt
import hashlib
from flask import Request
# I need to change the password on my luggage
SECRET_KEY="12345"
import string
import random

# 5 Minute Token timeout
# TODO: Make thie configurable, so "remember me" will make a much MUCH longer token
def encode_auth_token(user_id):
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=300),
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
    print("Random string of length", length, "is:", result_str)
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
    pprint.pprint(auth_token)
    if auth_token:
        try:
            resp = decode_auth_token(auth_token,SECRET_KEY)
            pprint.pprint(resp)
            print("Cookies")
            pprint.pprint(request.cookies)
            if resp:
                if 'mspysid' in request.cookies:
                    session = request.cookies['mspysid']
                    m = hashlib.sha256()
                    if session is not None:
                        m.update(session.encode('utf-8'))
                        if m.hexdigest() != resp['session']:
                            print('Invalid hex')
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
        print('Path:')
        pprint.pprint(request.path)
        print("Done",flush=True)
        auth_token = getAuthToken(request)
        jwt = getJwt(request)
        if jwt is None:
            return jsonify({'status':'failure','error':'Null session'}),401
        pprint.pprint(jwt)
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
                    return jsonify({'status':'failure','error':'Invalid permissions'}),401
        else:
            return func(*args,**kwargs)
    wrapper_jwt_private.__name__ = func.__name__
    return wrapper_jwt_private
    
