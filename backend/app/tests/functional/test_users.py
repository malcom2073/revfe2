import pprint
import auth
import json
import core
USER="malcom2073"
PASSWORD="12345"
DEFAULTGROUPS=3
DEFAULTUSERS=2
from tests.functional.test_auth import get_valid_token
from tests.utils import getUsersSucceed, getUsersFail, getUsersAdminSucceed, getUsersAdminFail, validate_user

# Test noauth for every endpoint
# Test for the initial state of the endpoint
# Test creating
# Test destroying

def test_noauth_userslist(client):
    response = client.get("/api/users")
    jsonresponse = json.loads(response.data)
    assert jsonresponse[core.STATUS_KEY] == core.FAIL_STR
    assert jsonresponse[core.ERROR_KEY] == "Null session"


def test_initial_users(client):
    authheaders = get_valid_token(client)
    jsonresponse = getUsersSucceed(client,authheaders)
    assert len(jsonresponse["users"]) == DEFAULTUSERS # 2 test users by default.


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

def addUserPermission(client,authheaders,clientid,permissionstr):
    authheaders = get_valid_token(client)
    rv = client.patch('/api/users/' + str(clientid),headers=authheaders,json={ 'add-group':['Members'] })
    jsonresponse = json.loads(rv.data)
    print("addUserPermission",flush=True)
    pprint.pprint(jsonresponse)
    assert jsonresponse[core.STATUS_KEY] == core.SUCCESS_STR

def test_usertest(client):
    newclientid = test_create_user(client)
    authheaders = get_valid_token(client)
    pprint.pprint("AuthHeaders")
    pprint.pprint(authheaders)
    
    validate_user(client,newclientid)
    clientauthheaders = get_valid_token(client,"test1","asdf")
    pprint.pprint("ClientAuthHeaders")
    pprint.pprint(clientauthheaders)
    getUsersFail(client,clientauthheaders)
    authheaders = get_valid_token(client)
    addUserPermission(client,authheaders,newclientid,'members')
    clientauthheaders = get_valid_token(client,"test1","asdf")
    getUsersSucceed(client,clientauthheaders,newclientid)


# Verify we can't authenticat if we're not validated.
def test_newuser_validation(client):
    newclientid = test_create_user(client)
    rv = client.post('/api/authenticate',json={ 'username': "test1", 'password': "asdf" })
    jsonresponse = json.loads(rv.data)
    pprint.pprint(jsonresponse)
    assert jsonresponse[core.STATUS_KEY] == core.FAIL_STR
    validate_user(client,newclientid)
    newclientid = get_valid_token(client,"test1","asdf")

    # Verify the password worked and we have a token
#    print("AUTH JSON RESPONSE")
#    pprint.pprint(jsonresponse)
#    #assert jsonresponse[core.STATUS_KEY] == core.SUCCESS_STR

# Test to make sure a validated non-admin user can't access things like /api/users to list all users.
def test_user_perms(client):
    newclientid = test_create_user(client)
    validate_user(client,newclientid)
    authheaders = get_valid_token(client,"test1","asdf")
    getUsersFail(client,authheaders)
#    getUsersSucceed(client,authheaders,newclientid)
#    assert False

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


