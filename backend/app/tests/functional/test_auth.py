import pprint
import auth
import json
import core
USER="malcom2073"
PASSWORD="12345"
def get_valid_token(client,username=USER,password=PASSWORD):
    # Authenticate to get our token
    rv = client.post('/api/authenticate',json={ 'username': username, 'password': password })
    jsonresponse = json.loads(rv.data)

    # Verify the password worked and we have a token
#    print("AUTH JSON RESPONSE")
#    pprint.pprint(jsonresponse)
#    #assert jsonresponse[core.STATUS_KEY] == core.SUCCESS_STR
    assert 'access_token' in jsonresponse
    accesstoken = jsonresponse['access_token']
    assert 'Set-Cookie' in rv.headers
    cookie = rv.headers['Set-Cookie']
    return {'Set-Cookie':cookie,'Authorization':'Bearer ' + accesstoken}



def getUser(client,clientid,authheaders):
    response = client.get("/api/users/" + str(clientid),headers=authheaders)
    jsonresponse = json.loads(response.data)
    return jsonresponse

def test_users_noauth(client):
    response = client.get("/api/users")
    jsonresponse = json.loads(response.data)
    assert jsonresponse[core.STATUS_KEY] == core.FAIL_STR
    assert jsonresponse[core.ERROR_KEY] == "Null session"

def test_initial_users(client):
    authheaders = get_valid_token(client)
    response = client.get("/api/users",headers=authheaders)
    jsonresponse = json.loads(response.data)
    assert jsonresponse[core.STATUS_KEY] == core.SUCCESS_STR
    assert len(jsonresponse["users"]) == 2 # 2 test users by default.

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
    jsonresponse = getUser(client,clientid,authheaders)
    assert jsonresponse[core.STATUS_KEY] == core.SUCCESS_STR
    assert len(jsonresponse['users']) == 1
    assert 'username' in jsonresponse['users'][0] and jsonresponse['users'][0]['username'] == "test1"
    response = client.get("/api/users",headers=authheaders)
    jsonresponse = json.loads(response.data)
    pprint.pprint(jsonresponse)
    assert jsonresponse[core.STATUS_KEY] == core.SUCCESS_STR
    assert len(jsonresponse["users"]) == 3 # 2 test users by default.
    return clientid

def test_edit_user(client):
    newclientid = test_create_user(client)
    authheaders = get_valid_token(client)
    # response = client.get("/api/users",headers=authheaders)
    # jsonresponse = json.loads(response.data)
    # pprint.pprint(jsonresponse)
    # assert jsonresponse[core.STATUS_KEY] == core.SUCCESS_STR
    # assert len(jsonresponse["users"]) == 3 # 2 test users by default.
    response = client.patch("/api/users/" + str(newclientid),headers=authheaders,json={
        "email":"newemail"
    })
    jsonresponse = json.loads(response.data)
    assert jsonresponse[core.STATUS_KEY] == core.SUCCESS_STR
    assert 'users' in jsonresponse
    assert jsonresponse['users'][0]['email'] == "newemail"
    #assert False


def test_auth(client):
    get_valid_token(client)