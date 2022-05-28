import pprint
import auth
import json
import core
USER="malcom2073"
PASSWORD="12345"
DEFAULTGROUPS=3
DEFAULTUSERS=2
from tests.utils import getUsersSucceed, getUsersFail, getUsersAdminSucceed, getUsersAdminFail, validate_user,getPermissions,get_valid_token,createUser,createPermission
from tests.utils import addPermissionToGroup,addGroupToUser,createGroup,getGroups



def test_noauth_grouplist(client):
    response = client.get("/api/groups")
    jsonresponse = json.loads(response.data)
    assert jsonresponse[core.STATUS_KEY] == core.FAIL_STR
    assert jsonresponse[core.ERROR_KEY] == "Null session"

def test_initial_groups(client):
    authheaders = get_valid_token(client)
    jsonresponse = getGroups(client,authheaders)
    assert len(jsonresponse) == DEFAULTGROUPS # 2 test users by default.

def test_create_group(client):
    authheaders = get_valid_token(client)
    groupresponse = createGroup(client,authheaders,"testgroup")
    groupid = groupresponse['id']
    groupslist = getGroups(client,authheaders,groupid)
    pprint.pprint(groupid)
    pprint.pprint(groupslist)
    assert 'name' in groupslist[0] and groupslist[0]['name'] == "testgroup"
    fullgroupslist = getGroups(client,authheaders)
    assert len(fullgroupslist) == DEFAULTGROUPS+1 # 2 test users by default.

def test_edit_group(client):
    authheaders = get_valid_token(client)
    groupresponse = createGroup(client,authheaders,"testgroup")
    response = client.patch("/api/groups/" + str(groupresponse['id']),headers=authheaders,json={
        "name":"testgrouptwo"
    })
    jsonresponse = json.loads(response.data)
    assert jsonresponse[core.STATUS_KEY] == core.SUCCESS_STR
    assert 'groups' in jsonresponse
    assert jsonresponse['groups'][0]['name'] == "testgrouptwo"

