import pprint
import auth
import json
import core
DEFAULTGROUPS=3
DEFAULTUSERS=2
from tests.utils import getUsersSucceed, getUsersFail, getUsersAdminSucceed, getUsersAdminFail, validate_user,get_valid_token






def test_auth(client):
    get_valid_token(client)

