import pprint
import auth
import json
import core
USER="malcom2073"
PASSWORD="12345"
DEFAULTGROUPS=2
DEFAULTUSERS=2
def get_valid_token(client,username=USER,password=PASSWORD):
    # Authenticate to get our token
    rv = client.post('/api/authenticate',json={ 'username': username, 'password': password })
    jsonresponse = json.loads(rv.data)

    # Verify the password worked and we have a token
#    print("AUTH JSON RESPONSE")
#    pprint.pprint(jsonresponse)
#    #assert jsonresponse[core.STATUS_KEY] == core.SUCCESS_STR
    print("Testing get_valid_token")
    assert jsonresponse[core.STATUS_KEY] == core.SUCCESS_STR
    assert 'access_token' in jsonresponse
    accesstoken = jsonresponse['access_token']
    assert 'Set-Cookie' in rv.headers
    cookie = rv.headers['Set-Cookie']
    return {'Set-Cookie':cookie,'Authorization':'Bearer ' + accesstoken}



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


def test_noauth_userslist(client):
    response = client.get("/api/users")
    jsonresponse = json.loads(response.data)
    assert jsonresponse[core.STATUS_KEY] == core.FAIL_STR
    assert jsonresponse[core.ERROR_KEY] == "Null session"

def test_noauth_grouplist(client):
    response = client.get("/api/groups")
    jsonresponse = json.loads(response.data)
    assert jsonresponse[core.STATUS_KEY] == core.FAIL_STR
    assert jsonresponse[core.ERROR_KEY] == "Null session"

def test_initial_users(client):
    authheaders = get_valid_token(client)
    jsonresponse = getUsersSucceed(client,authheaders)
    assert len(jsonresponse["users"]) == DEFAULTUSERS # 2 test users by default.


def test_initial_groups(client):
    authheaders = get_valid_token(client)
    jsonresponse = getGroupsSucceed(client,authheaders)
    assert len(jsonresponse["groups"]) == DEFAULTGROUPS # 2 test users by default.

def test_create_user(client):
    authheaders = get_valid_token(client)
    response = client.post("/api/users",headers=authheaders,json={
        "username":"test1",
        "name":"test1",
        "email":"admin",
        "password":"asdf",
        "state":"unknown"})
    jsonresponse = json.loads(response.data)
    assert 'result' in jsonresponse
    assert 'id' in jsonresponse['result']
    clientid = jsonresponse['result']['id']
    jsonresponse = getUsersAdminSucceed(client,authheaders,clientid)
    pprint.pprint(jsonresponse)
    assert jsonresponse[core.STATUS_KEY] == core.SUCCESS_STR
    assert len(jsonresponse['users']) == 1
    assert 'username' in jsonresponse['users'][0] and jsonresponse['users'][0]['username'] == "test1"
    response = client.get("/api/users",headers=authheaders)
    jsonresponse = json.loads(response.data)
    print("Created user")
    pprint.pprint(jsonresponse)
    assert jsonresponse[core.STATUS_KEY] == core.SUCCESS_STR
    assert len(jsonresponse["users"]) == 3 # 2 test users by default.
    return clientid

# Test to make sure a validated non-admin user can't access things like /api/users to list all users.
def test_user_perms(client):
    newclientid = test_create_user(client)
    validate_user(client,newclientid)
    authheaders = get_valid_token(client,"test1","asdf")
    getUsersFail(client,authheaders)
#    assert False
def validate_user(client,userid):
    authheaders = get_valid_token(client)
    response = client.patch("/api/users/" + str(userid),headers=authheaders,json={
        "validated":True
    })
    jsonresponse = json.loads(response.data)
    assert jsonresponse[core.STATUS_KEY] == core.SUCCESS_STR
    assert 'users' in jsonresponse
    assert jsonresponse['users'][0]['validated'] == True

def test_newuser_validation(client):
    newclientid = test_create_user(client)
    rv = client.post('/api/authenticate',json={ 'username': "test1", 'password': "asdf" })
    jsonresponse = json.loads(rv.data)
    pprint.pprint(jsonresponse)
    assert jsonresponse[core.STATUS_KEY] == core.FAIL_STR
    validate_user(client,newclientid)

    # Verify the password worked and we have a token
#    print("AUTH JSON RESPONSE")
#    pprint.pprint(jsonresponse)
#    #assert jsonresponse[core.STATUS_KEY] == core.SUCCESS_STR

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

def test_edit_user(client):
    newclientid = test_create_user(client)
    authheaders = get_valid_token(client)
    response = client.patch("/api/users/" + str(newclientid),headers=authheaders,json={
        "email":"newemail"
    })
    jsonresponse = json.loads(response.data)
    assert jsonresponse[core.STATUS_KEY] == core.SUCCESS_STR
    assert 'users' in jsonresponse
    assert jsonresponse['users'][0]['email'] == "newemail"



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


def test_auth(client):
    get_valid_token(client)

