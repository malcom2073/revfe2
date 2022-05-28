import core
import json
import pprint

USER="malcom2073"
PASSWORD="12345"

def get_valid_token(client,username=USER,password=PASSWORD):
    # Authenticate to get our token
    rv = client.post('/api/authenticate',json={ 'username': username, 'password': password })
    jsonresponse = json.loads(rv.data)
    assert jsonresponse[core.STATUS_KEY] == core.SUCCESS_STR
    assert 'access_token' in jsonresponse
    accesstoken = jsonresponse['access_token']
    assert 'Set-Cookie' in rv.headers
    cookie = rv.headers['Set-Cookie']
    return {'Set-Cookie':cookie,'Authorization':'Bearer ' + accesstoken}


def createPermission(client,authheaders,permname,desc,succeed=True):
    response = client.post("/api/permissions",headers=authheaders,json={
        "name":permname,
        "description":desc
    })
    jsonresponse = json.loads(response.data)
    if succeed:
        assert jsonresponse[core.STATUS_KEY] == core.SUCCESS_STR
        return jsonresponse['permission']
    else:
        assert jsonresponse[core.STATUS_KEY] == core.FAIL_STR
        return jsonresponse


def getPermissions(client,authheaders,succeed=True,permid=None):
    print("getPermissionsSucceed")
    if permid == None:
        response = client.get("/api/permissions",headers=authheaders)
        jsonresponse = json.loads(response.data)
        assert core.STATUS_KEY in jsonresponse
        pprint.pprint(jsonresponse)
        if succeed:
            assert jsonresponse[core.STATUS_KEY] == core.SUCCESS_STR
        else:
            assert jsonresponse[core.STATUS_KEY] == core.FAIL_STR
        return jsonresponse
    else:
        response = client.get("/api/permissions/" + str(permid),headers=authheaders)
        jsonresponse = json.loads(response.data)
        assert core.STATUS_KEY in jsonresponse
        if succeed:
            assert jsonresponse[core.STATUS_KEY] == core.SUCCESS_STR
        else:
            assert jsonresponse[core.STATUS_KEY] == core.FAIL_STR
        return jsonresponse

def addPermissionToGroup(client,authheaders,groupid,permname,success=True):
    response = client.patch("/api/groups/" + str(groupid),headers=authheaders,json={ 'add-permission':[permname] })
    jsonresponse = json.loads(response.data)
    assert core.STATUS_KEY in jsonresponse
    if success:
        assert jsonresponse[core.STATUS_KEY] == core.SUCCESS_STR
    else:
        assert jsonresponse[core.STATUS_KEY] == core.FAIL_STR
def addGroupToUser(client,authheaders,userid,groupname,success=True):
    response = client.patch("/api/users/" + str(userid),headers=authheaders,json={ 'add-group':[groupname] })
    jsonresponse = json.loads(response.data)
    assert core.STATUS_KEY in jsonresponse
    if success:
        assert jsonresponse[core.STATUS_KEY] == core.SUCCESS_STR
    else:
        assert jsonresponse[core.STATUS_KEY] == core.FAIL_STR
def createGroup(client,authheaders,groupname):
    response = client.post("/api/groups",headers=authheaders,json={
        "name":groupname})
    jsonresponse = json.loads(response.data)
    assert core.STATUS_KEY in jsonresponse
    assert jsonresponse[core.STATUS_KEY] == core.SUCCESS_STR
    assert 'id' in jsonresponse['group']
    groupid = jsonresponse['group']['id']
    groupjson = getGroups(client,authheaders,groupid)
    found = False
    for group in groupjson:
        if group['name'] == groupname:
            found = True
    assert found
    return jsonresponse['group']


def createUser(client,authheaders,userjson,succeed=True):
    response = client.post("/api/users",headers=authheaders,json=userjson)
    jsonresponse = json.loads(response.data)
    assert core.STATUS_KEY in jsonresponse
    if succeed:
        assert jsonresponse[core.STATUS_KEY] == core.SUCCESS_STR
        assert 'id' in jsonresponse['users'][0]
        return jsonresponse['users'][0]
    else:
        assert jsonresponse[core.STATUS_KEY] == core.FAIL_STR
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


def validate_user(client,authheaders,userid):
    response = client.patch("/api/users/" + str(userid),headers=authheaders,json={
        "validated":True
    })
    jsonresponse = json.loads(response.data)
    assert jsonresponse[core.STATUS_KEY] == core.SUCCESS_STR
    assert 'users' in jsonresponse
    assert jsonresponse['users'][0]['validated'] == True
def getGroups(client,authheaders,groupid=None,success=True):
    if groupid == None:
        response = client.get("/api/groups",headers=authheaders)
        jsonresponse = json.loads(response.data)
        assert core.STATUS_KEY in jsonresponse
        if success:
            assert jsonresponse[core.STATUS_KEY] == core.SUCCESS_STR
            return jsonresponse['groups']
        else:
            assert jsonresponse[core.STATUS_KEY] == core.FAIL_STR
            return jsonresponse
    else:
        response = client.get("/api/groups/" + str(groupid),headers=authheaders)
        jsonresponse = json.loads(response.data)
        assert core.STATUS_KEY in jsonresponse
        if success:
            assert jsonresponse[core.STATUS_KEY] == core.SUCCESS_STR
            return jsonresponse['groups']
        else:
            assert jsonresponse[core.STATUS_KEY] == core.FAIL_STR
            return jsonresponse
