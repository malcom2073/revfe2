import pprint
import auth
import json
import core

def getUser(client,clientid):
    response = client.get("/api/users/" + str(clientid))
    jsonresponse = json.loads(response.data)
    return jsonresponse
def test_empty_users(client):
    response = client.get("/api/users")
    jsonresponse = json.loads(response.data)
    pprint.pprint(jsonresponse)
    assert jsonresponse[core.STATUS_KEY] == core.SUCCESS_STR
    assert len(jsonresponse["users"]) == 2 # 2 test users by default.
    #assert False


def test_create_user(client):
    response = client.post("/api/users",json={
        "username":"test1",
        "name":"test1",
        "email":"admin",
        "password":"asdf",
        "state":"unknown"})
    pprint.pprint(response.data)
    jsonresponse = json.loads(response.data)
    jsonresponse = getUser(client,jsonresponse['result']['id'])
    pprint.pprint(jsonresponse)
    response = client.get("/api/users")
    jsonresponse = json.loads(response.data)
    pprint.pprint(jsonresponse)
    assert jsonresponse[core.STATUS_KEY] == core.SUCCESS_STR
    assert len(jsonresponse["users"]) == 3 # 2 test users by default.

