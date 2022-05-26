import core
import json
import pprint

from tests.functional.test_auth import get_valid_token


def getPermissionsSucceed(client,authheaders,permid=None):
    print("getPermissionsSucceed")
    if permid == None:
        response = client.get("/api/permissions",headers=authheaders)
        jsonresponse = json.loads(response.data)
        assert core.STATUS_KEY in jsonresponse
        pprint.pprint(jsonresponse)
        assert jsonresponse[core.STATUS_KEY] == core.SUCCESS_STR
        return jsonresponse
    else:
        response = client.get("/api/permissions/" + str(permid),headers=authheaders)
        jsonresponse = json.loads(response.data)
        assert core.STATUS_KEY in jsonresponse
        assert jsonresponse[core.STATUS_KEY] == core.SUCCESS_STR
        return jsonresponse

def getUsersSucceed(client,authheaders,clientid=None):
    if clientid == None:
        response = client.get("/api/users",headers=authheaders)
        jsonresponse = json.loads(response.data)
        assert core.STATUS_KEY in jsonresponse
        print("getUsersSucceed")
        pprint.pprint(jsonresponse)
        assert jsonresponse[core.STATUS_KEY] == core.SUCCESS_STR
        return jsonresponse
    else:
        response = client.get("/api/users/" + str(clientid),headers=authheaders)
        jsonresponse = json.loads(response.data)
        assert core.STATUS_KEY in jsonresponse
        assert jsonresponse[core.STATUS_KEY] == core.SUCCESS_STR
        return jsonresponse

def getUsersFail(client,authheaders,clientid=None):
    if clientid == None:
        response = client.get("/api/users",headers=authheaders)
        jsonresponse = json.loads(response.data)
        assert core.STATUS_KEY in jsonresponse
        assert jsonresponse[core.STATUS_KEY] == core.FAIL_STR
        return jsonresponse
    else:
        response = client.get("/api/users/" + str(clientid),headers=authheaders)
        jsonresponse = json.loads(response.data)
        assert core.STATUS_KEY in jsonresponse
        assert jsonresponse[core.STATUS_KEY] == core.FAIL_STR
        return jsonresponse


def getUsersAdminSucceed(client,authheaders,clientid=None):
    response = client.get("/api/admin/users/" + str(clientid),headers=authheaders)
    jsonresponse = json.loads(response.data)
    assert core.STATUS_KEY in jsonresponse
    assert jsonresponse[core.STATUS_KEY] == core.SUCCESS_STR
    return jsonresponse

def getUsersAdminFail(client,authheaders,clientid=None):
    response = client.get("/api/admin/users/" + str(clientid),headers=authheaders)
    jsonresponse = json.loads(response.data)
    assert core.STATUS_KEY in jsonresponse
    assert jsonresponse[core.STATUS_KEY] == core.FAIL_STR
    return jsonresponse


def validate_user(client,userid):
    authheaders = get_valid_token(client)
    response = client.patch("/api/users/" + str(userid),headers=authheaders,json={
        "validated":True
    })
    jsonresponse = json.loads(response.data)
    assert jsonresponse[core.STATUS_KEY] == core.SUCCESS_STR
    assert 'users' in jsonresponse
    assert jsonresponse['users'][0]['validated'] == True
