import core
import auth.endpoints.userendpoint as userendpoint
import auth.endpoints.groupendpoint as groupendpoint
import auth.endpoints.useradminendpoint as useradminendpoint
from auth.endpoints.authendpoint import Authenticate
from auth.endpoints.authendpoint import Renew
from auth.endpoints.permissionendpoint import PermissionEndpoint
core.app.add_url_rule("/api/users/<userid>", view_func=userendpoint.UserEndpoint.as_view("example_api"))
core.app.add_url_rule("/api/users", view_func=userendpoint.UserEndpoint.as_view("example_apis"))
core.app.add_url_rule("/api/permissions/<permissionid>", view_func=PermissionEndpoint.as_view("permissionapi"))
core.app.add_url_rule("/api/permissions", view_func=PermissionEndpoint.as_view("permissionapis"))


core.app.add_url_rule("/api/admin/users/<userid>", view_func=useradminendpoint.UserAdminEndpoint.as_view("example_adminapi"))
core.app.add_url_rule("/api/admin/users", view_func=useradminendpoint.UserAdminEndpoint.as_view("example_adminapis"))


core.app.add_url_rule("/api/groups/<groupid>", view_func=groupendpoint.GroupEndpoint.as_view("group_api"))
core.app.add_url_rule("/api/groups", view_func=groupendpoint.GroupEndpoint.as_view("groups_api"))


core.app.add_url_rule("/api/auth/authenticate", view_func=Authenticate.as_view("example_apisauth"))
core.app.add_url_rule("/api/auth/renew", view_func=Renew.as_view("example_apisauthrenew"))
