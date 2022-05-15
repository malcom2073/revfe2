import core
import auth.endpoints.userendpoint as userendpoint

core.app.add_url_rule("/api/users/<userid>", view_func=userendpoint.UserEndpoint.as_view("example_api"))
core.app.add_url_rule("/api/users", view_func=userendpoint.UserEndpoint.as_view("example_apis"))

