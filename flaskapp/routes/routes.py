from flaskapp.routes.index.index import IndexApi
from flaskapp.routes.user.login import LoginApi
from flaskapp.routes.user.logout import LogoutApi
from flaskapp.routes.user.register import RegisterApi
from flaskapp.routes.user.properties import PropertiesApi
from flaskapp.routes.user.profile import ProfileApi
from flaskapp.routes.place.debug_place import DebugPlaceApi
from flaskapp.routes.friend_requests.friends import FriendsApi
from flaskapp.routes.friend_requests.friend_request import FriendRequestApi, FriendRequestsApi


def initialize_routes(api):
    api.add_resource(RegisterApi, '/user/register')
    api.add_resource(LoginApi, '/user/login')
    api.add_resource(LogoutApi, '/user/logout')
    api.add_resource(PropertiesApi, '/user/properties')
    api.add_resource(ProfileApi, '/user/<user_id>')
    api.add_resource(IndexApi, '/')
    api.add_resource(DebugPlaceApi, "/place/debug_places")
    api.add_resource(FriendsApi, "/user/friends")
    api.add_resource(FriendRequestApi, "/user/friend_request")
    api.add_resource(FriendRequestsApi, "/user/friend_requests")