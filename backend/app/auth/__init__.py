import core
import auth.endpoints.userendpoint as userendpoint

core.app.add_url_rule("/api/users/<userid>", view_func=userendpoint.UserEndpoint.as_view("example_api"))
core.app.add_url_rule("/api/users", view_func=userendpoint.UserEndpoint.as_view("example_apis"))

from auth.endpoints.authendpoint import Authenticate
from auth.endpoints.authendpoint import Renew

core.app.add_url_rule("/api/authenticate", view_func=Authenticate.as_view("example_apisauth"))
core.app.add_url_rule("/api/renew", view_func=Renew.as_view("example_apisauthrenew"))
