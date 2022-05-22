from flask.views import MethodView
from flask import request
import db
from auth.models.user import User
from auth.models.group import Group
import pprint
import reactive_flask
from core import SUCCESS_STR
from core import FAIL_STR
from core import STATUS_KEY
from core import ERROR_KEY

# /users/<userid>
class UserEndpoint(MethodView):

    @reactive_flask.jwt_private
    def get(self,userid=None):
        """
        Endpoint to get a specific user
        This is using docstrings for specifications.
        ---
        parameters:
            - in: path
              name: userid
              schema:
                  type: integer
              required: true
        responses:
            200:
                description: A user object
            401:
                description: Permission denied
        """
        #        users = manager.getAllUsers()
        if userid:
            dbsession = db.AppSession()
            user = dbsession.query(User).filter(User.id == userid).first()
            pprint.pprint(user)
            if user is None:
                return {STATUS_KEY:FAIL_STR,ERROR_KEY:"No valid User for userid " + str(userid) + " found"},200
            return {STATUS_KEY:SUCCESS_STR,'users':[user.as_obj()]},200
        dbsession = db.AppSession()
        users = dbsession.query(User).all()
        pprint.pprint(users)
        if users is None:
            return {STATUS_KEY:FAIL_STR,ERROR_KEY:"No valid User for userid " + str(userid) + " found"},200
        return {STATUS_KEY:SUCCESS_STR,'users':[user.as_obj() for user in users]},200

    @reactive_flask.jwt_private
    def post(self,userid=None):
       
        userjson = request.get_json()
        dbsession = db.AppSession()
        user = User(userjson['name'],userjson['username'],userjson['email'],userjson['password'],[],False)
        dbsession.add(user)
        dbsession.commit()
        return {'result':SUCCESS_STR,'result':{'id' : user.id, 'username':user.username,'name': user.name,'password':user.password}},200

    @reactive_flask.jwt_private    
    def put(self):
        """ Responds to PUT requests """
        return "Responding to a PUT request"

    @reactive_flask.jwt_private    
    def patch(self,userid):
        """ Responds to PATCH requests """
        dbsession = db.AppSession()
        user = dbsession.query(User).filter(User.id == userid).first()
        pprint.pprint(user)
        if user is None:
            return {STATUS_KEY:FAIL_STR,ERROR_KEY:"No valid User for userid " + str(userid) + " found"},200
        userjson = request.get_json()
        # This will contain the changes to make tothis use as list of  KVP
        # [{"key":"value"}]
        print(userjson)
        for patch in userjson:
            #pprint.pprint(patch)
            print(patch)
            setattr(user,patch,userjson[patch])
#            user[patch] = userjson[patch]
        try:
            dbsession.commit()
            return {STATUS_KEY:SUCCESS_STR,'users':[user.as_obj()]},200
        except:
            dbsession.rollback()
            return {STATUS_KEY:FAIL_STR,ERROR_KEY:"Unable to commit!"},200

        return "Responding to a PATCH request"

    @reactive_flask.jwt_private
    def delete(self):
        """ Responds to DELETE requests """
        return "Responding to a DELETE request"


