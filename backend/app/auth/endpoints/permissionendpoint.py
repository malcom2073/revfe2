from flask.views import MethodView
from flask import request
import db
from auth.models.user import User
from auth.models.group import Group
from auth.models.permission import Permission
import pprint
import reactive_flask
from core import SUCCESS_STR
from core import FAIL_STR
from core import STATUS_KEY
from core import ERROR_KEY

# /users/<userid>
class PermissionEndpoint(MethodView):

    @reactive_flask.jwt_private
    def get(self,permid=None):
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
        if permid:
            dbsession = db.AppSession()
            perm = dbsession.query(Permission).filter(Permission.id == permid).first()
            pprint.pprint(perm)
            if perm is None:
                return {STATUS_KEY:FAIL_STR,ERROR_KEY:"No valid Permission for permid " + str(permid) + " found"},200
            return {STATUS_KEY:SUCCESS_STR,'permissions':[perm.as_obj()]},200
        dbsession = db.AppSession()
        perms = dbsession.query(Group).all()
        pprint.pprint(perms)
        if perms is None:
            return {STATUS_KEY:FAIL_STR,ERROR_KEY:"No valid Permission for permid " + str(permid) + " found"},200
        return {STATUS_KEY:SUCCESS_STR,'permissions':[perm.as_obj() for perm in perms]},200

    @reactive_flask.jwt_private
    def post(self,permid=None):
       
        permjson = request.get_json()
        dbsession = db.AppSession()
        perm = Permission(permjson['name'],permjson['description'])
        dbsession.add(perm)
        dbsession.commit()
        return {'result':SUCCESS_STR,'result':{'id' : perm.id, 'name':perm.name,'description':perm.description}},200

    @reactive_flask.jwt_private    
    def put(self):
        """ Responds to PUT requests """
        return "Responding to a PUT request"

    @reactive_flask.jwt_private    
    def patch(self,permid):
        """ Responds to PATCH requests """
        dbsession = db.AppSession()
        perm = dbsession.query(Permission).filter(Permission.id == permid).first()
        pprint.pprint(perm)
        if perm is None:
            return {STATUS_KEY:FAIL_STR,ERROR_KEY:"No valid Permission for permid " + str(permid) + " found"},200
        permjson = request.get_json()
        # This will contain the changes to make tothis use as list of  KVP
        # [{"key":"value"}]
        print(permjson)
        for patch in permjson:
            #pprint.pprint(patch)
            print(patch)
            setattr(perm,patch,permjson[patch])
#            user[patch] = userjson[patch]
        try:
            dbsession.commit()
            return {STATUS_KEY:SUCCESS_STR,'permissions':[perm.as_obj()]},200
        except:
            dbsession.rollback()
            return {STATUS_KEY:FAIL_STR,ERROR_KEY:"Unable to commit!"},200

        return "Responding to a PATCH request"

    @reactive_flask.jwt_private
    def delete(self):
        """ Responds to DELETE requests """
        return "Responding to a DELETE request"


