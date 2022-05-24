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
class GroupEndpoint(MethodView):

    @reactive_flask.jwt_private
    def get(self,groupid=None):
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
        if groupid:
            dbsession = db.AppSession()
            user = dbsession.query(Group).filter(Group.id == groupid).first()
            pprint.pprint(user)
            if user is None:
                return {STATUS_KEY:FAIL_STR,ERROR_KEY:"No valid Group for groupid " + str(groupid) + " found"},200
            return {STATUS_KEY:SUCCESS_STR,'groups':[user.as_obj()]},200
        dbsession = db.AppSession()
        groups = dbsession.query(Group).all()
        pprint.pprint(groups)
        if groups is None:
            return {STATUS_KEY:FAIL_STR,ERROR_KEY:"No valid User for groupid " + str(groupid) + " found"},200
        return {STATUS_KEY:SUCCESS_STR,'groups':[group.as_obj() for group in groups]},200

    @reactive_flask.jwt_private
    def post(self,groupid=None):
       
        groupjson = request.get_json()
        dbsession = db.AppSession()
        group = Group(groupjson['name'])
        dbsession.add(group)
        dbsession.commit()
        return {'result':SUCCESS_STR,'result':{'id' : group.id, 'name':group.name}},200

    @reactive_flask.jwt_private    
    def put(self):
        """ Responds to PUT requests """
        return "Responding to a PUT request"

    @reactive_flask.jwt_private    
    def patch(self,groupid):
        """ Responds to PATCH requests """
        dbsession = db.AppSession()
        group = dbsession.query(Group).filter(Group.id == groupid).first()
        pprint.pprint(group)
        if group is None:
            return {STATUS_KEY:FAIL_STR,ERROR_KEY:"No valid User for userid " + str(groupid) + " found"},200
        groupjson = request.get_json()
        # This will contain the changes to make tothis use as list of  KVP
        # [{"key":"value"}]
        print(groupjson)
        for patch in groupjson:
            #pprint.pprint(patch)
            print(patch)
            setattr(group,patch,groupjson[patch])
#            user[patch] = userjson[patch]
        try:
            dbsession.commit()
            return {STATUS_KEY:SUCCESS_STR,'groups':[group.as_obj()]},200
        except:
            dbsession.rollback()
            return {STATUS_KEY:FAIL_STR,ERROR_KEY:"Unable to commit!"},200

        return "Responding to a PATCH request"

    @reactive_flask.jwt_private
    def delete(self):
        """ Responds to DELETE requests """
        return "Responding to a DELETE request"


