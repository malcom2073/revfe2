import core
import auth.endpoints.userendpoint as userendpoint
import auth.endpoints.groupendpoint as groupendpoint
core.app.add_url_rule("/api/users/<userid>", view_func=userendpoint.UserEndpoint.as_view("example_api"))
core.app.add_url_rule("/api/users", view_func=userendpoint.UserEndpoint.as_view("example_apis"))


import auth.endpoints.useradminendpoint as useradminendpoint
core.app.add_url_rule("/api/admin/users/<userid>", view_func=useradminendpoint.UserAdminEndpoint.as_view("example_adminapi"))
core.app.add_url_rule("/api/admin/users", view_func=useradminendpoint.UserAdminEndpoint.as_view("example_adminapis"))


core.app.add_url_rule("/api/groups/<groupid>", view_func=groupendpoint.GroupEndpoint.as_view("group_api"))
core.app.add_url_rule("/api/groups", view_func=groupendpoint.GroupEndpoint.as_view("groups_api"))

from auth.endpoints.authendpoint import Authenticate
from auth.endpoints.authendpoint import Renew

core.app.add_url_rule("/api/authenticate", view_func=Authenticate.as_view("example_apisauth"))
core.app.add_url_rule("/api/renew", view_func=Renew.as_view("example_apisauthrenew"))
