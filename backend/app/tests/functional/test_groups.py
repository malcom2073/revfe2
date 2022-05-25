import pprint
import auth
import json
import core
USER="malcom2073"
PASSWORD="12345"
DEFAULTGROUPS=3
DEFAULTUSERS=2
from tests.functional.test_auth import get_valid_token


def getGroupsSucceed(client,authheaders,groupid=None):
    if groupid == None:
        response = client.get("/api/groups",headers=authheaders)
        jsonresponse = json.loads(response.data)
        assert core.STATUS_KEY in jsonresponse
        assert jsonresponse[core.STATUS_KEY] == core.SUCCESS_STR
        return jsonresponse
    else:
        response = client.get("/api/groups/" + str(groupid),headers=authheaders)
        jsonresponse = json.loads(response.data)
        assert core.STATUS_KEY in jsonresponse
        assert jsonresponse[core.STATUS_KEY] == core.SUCCESS_STR
        return jsonresponse

def test_noauth_grouplist(client):
    response = client.get("/api/groups")
    jsonresponse = json.loads(response.data)
    assert jsonresponse[core.STATUS_KEY] == core.FAIL_STR
    assert jsonresponse[core.ERROR_KEY] == "Null session"

def test_initial_groups(client):
    authheaders = get_valid_token(client)
    jsonresponse = getGroupsSucceed(client,authheaders)
    assert len(jsonresponse["groups"]) == DEFAULTGROUPS # 2 test users by default.

def test_create_group(client):
    authheaders = get_valid_token(client)
    response = client.post("/api/groups",headers=authheaders,json={
        "name":"testgroup"})
    jsonresponse = json.loads(response.data)
    assert 'result' in jsonresponse
    assert 'id' in jsonresponse['result']
    groupid = jsonresponse['result']['id']
    jsonresponse = getGroupsSucceed(client,authheaders,groupid)
    assert jsonresponse[core.STATUS_KEY] == core.SUCCESS_STR
    assert len(jsonresponse['groups']) == 1
    assert 'name' in jsonresponse['groups'][0] and jsonresponse['groups'][0]['name'] == "testgroup"
    response = client.get("/api/groups",headers=authheaders)
    jsonresponse = json.loads(response.data)
    pprint.pprint(jsonresponse)
    assert jsonresponse[core.STATUS_KEY] == core.SUCCESS_STR
    assert len(jsonresponse["groups"]) == DEFAULTGROUPS+1 # 2 test users by default.
    return groupid

def test_edit_group(client):
    newgroupid = test_create_group(client)
    authheaders = get_valid_token(client)
    response = client.patch("/api/groups/" + str(newgroupid),headers=authheaders,json={
        "name":"testgrouptwo"
    })
    jsonresponse = json.loads(response.data)
    assert jsonresponse[core.STATUS_KEY] == core.SUCCESS_STR
    assert 'groups' in jsonresponse
    assert jsonresponse['groups'][0]['name'] == "testgrouptwo"

