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
class UserEndpoint(MethodView):

    @reactive_flask.jwt_private
    @reactive_flask.requires_access_level(["users.list"])
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
        jwt = reactive_flask.getJwt(request)
        dbsession = db.AppSession()
        uid = jwt['user']['id']
        requser = dbsession.query(User).filter(User.id == uid).first()
        if not requser:
            return {STATUS_KEY:FAIL_STR,ERROR_KEY:"Requesting user is not valid!"}
#        if uid != userid:
#            if not requser.siteadmin:
#                # Check permissions here, are we allowed to retrieve users?
#            return {STATUS_KEY:FAIL_STR,ERROR_KEY:"Permission Denied"}
        if userid:
            user = dbsession.query(User).filter(User.id == userid).first()
            pprint.pprint(user)
            if user is None:
                return {STATUS_KEY:FAIL_STR,ERROR_KEY:"No valid User for userid " + str(userid) + " found"},200
            if uid != userid:
                return {STATUS_KEY:SUCCESS_STR,'users':[{'name':user.name,'email':user.email}]},200
            else:
                return {STATUS_KEY:SUCCESS_STR,'users':[user.as_obj()]},200
        dbsession = db.AppSession()
        users = dbsession.query(User).all()
        pprint.pprint(users)
        if users is None:
            return {STATUS_KEY:FAIL_STR,ERROR_KEY:"No valid User for userid " + str(userid) + " found"},200
        retval = []
        for user in users:
            retval.append({'name':user.name,'email':user.email})
        return {STATUS_KEY:SUCCESS_STR,'users':retval},200

    @reactive_flask.jwt_private
    def post(self,userid=None):
       
        userjson = request.get_json()
        dbsession = db.AppSession()
        #perms = dbsession.query(Permission).filter(Permission.name=="users.list").all()
        groups = dbsession.query(Group).filter(Group.name=="Newbie").all()
        user = User(userjson['name'],userjson['username'],userjson['email'],userjson['password'],groups,False)
        dbsession.add(user)
        dbsession.commit()
        return {STATUS_KEY:SUCCESS_STR,'users':[{'id' : user.id, 'username':user.username,'name': user.name,'password':user.password}]},200

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
            if 'add-group' == patch:
                for groupstr in userjson[patch]:
                    grouptoadd = groupstr
                    group = dbsession.query(Group).filter(Group.name == grouptoadd).first()
                    if group:
                        user.groups.append(group)
                    else:
                        dbsession.rollback()
                        return {STATUS_KEY:FAIL_STR,ERROR_KEY:"Unable to commit!"},200
            elif 'remove-group' == patch:
                pass
            else:
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


