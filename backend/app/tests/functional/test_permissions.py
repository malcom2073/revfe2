import pprint
import auth
import json
import core
USER="malcom2073"
PASSWORD="12345"
DEFAULTGROUPS=2
DEFAULTUSERS=2
DEFAULTPERMISSIONS=1
from tests.utils import getUsersSucceed, getUsersFail, getUsersAdminSucceed, getUsersAdminFail, validate_user,getPermissions,get_valid_token,createUser,createPermission
from tests.utils import addPermissionToGroup,addGroupToUser,createGroup
def test_noauth_permissionlist(client):
    response = client.get("/api/permissions")
    jsonresponse = json.loads(response.data)
    assert jsonresponse[core.STATUS_KEY] == core.FAIL_STR
    assert jsonresponse[core.ERROR_KEY] == "Null session"


def test_initial_permissions(client):
    authheaders = get_valid_token(client)
    jsonresponse = getPermissions(client,authheaders,True)
    assert len(jsonresponse["permissions"]) == DEFAULTPERMISSIONS # 2 test users by default.


def test_create_permission(client):
    authheaders = get_valid_token(client)
    newuser = createUser(client,authheaders,{
        "username":"test1",
        "name":"test1",
        "email":"admin",
        "password":"asdf",
        "state":"unknown"})
    validate_user(client,authheaders,newuser['id'])
    authheaders = get_valid_token(client,"test1","asdf")
    getPermissions(client,authheaders,False)
    authheaders = get_valid_token(client)
    newperm = createPermission(client,authheaders,"permissions.list","Perm list permission",True)
    newgroup = createGroup(client,authheaders,"testgroup")
    addPermissionToGroup(client,authheaders,newgroup['id'],newperm['name'])
    addGroupToUser(client,authheaders,newuser['id'],newgroup['name'])
    authheaders = get_valid_token(client,"test1","asdf")
    getPermissions(client,authheaders,True)
    #authheaders = get_valid_token(client)
