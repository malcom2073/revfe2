import pprint
import auth
import json
import core
USER="malcom2073"
PASSWORD="12345"
DEFAULTGROUPS=2
DEFAULTUSERS=2
DEFAULTPERMISSIONS=1
from tests.functional.test_auth import get_valid_token
from tests.utils import getUsersSucceed, getUsersFail, getUsersAdminSucceed, getUsersAdminFail, validate_user,getPermissionsSucceed

def test_noauth_permissionlist(client):
    response = client.get("/api/permissions")
    jsonresponse = json.loads(response.data)
    assert jsonresponse[core.STATUS_KEY] == core.FAIL_STR
    assert jsonresponse[core.ERROR_KEY] == "Null session"


def test_initial_permissions(client):
    authheaders = get_valid_token(client)
    jsonresponse = getPermissionsSucceed(client,authheaders)
    assert len(jsonresponse["permissions"]) == DEFAULTPERMISSIONS # 2 test users by default.


def test_create_permission(client):
    authheaders = get_valid_token(client)
    response = client.post("/api/permissions",headers=authheaders,json={
        "name":"test.permission",
        "description":"purely a test permission"
    })
    jsonresponse = json.loads(response.data)
    assert jsonresponse[core.STATUS_KEY] == core.SUCCESS_STR
