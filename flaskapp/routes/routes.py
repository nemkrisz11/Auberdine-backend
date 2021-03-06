from flaskapp.routes.index.index import IndexApi
from flaskapp.routes.user.login import LoginApi
from flaskapp.routes.user.logout import LogoutApi
from flaskapp.routes.user.register import RegisterApi
from flaskapp.routes.user.properties import PropertiesApi
from flaskapp.routes.user.profile import ProfileApi
from flaskapp.routes.friend_requests.friends import FriendsApi
from flaskapp.routes.friend_requests.friend_request import FriendRequestApi, FriendRequestsApi
from flaskapp.routes.user.search import UserSearchApi
from flaskapp.routes.place.get_place import GetPlaceApi
from flaskapp.routes.place.rate import RatePlaceApi
from flaskapp.routes.recommendation.recommendation import RecommendationApi


def initialize_routes(api):
    api.add_resource(RegisterApi, '/api/user/register')
    api.add_resource(LoginApi, '/api/user/login')
    api.add_resource(LogoutApi, '/api/user/logout')
    api.add_resource(PropertiesApi, '/api/user/properties')
    api.add_resource(ProfileApi, '/api/user/<user_id>')
    api.add_resource(IndexApi, '/api')
    api.add_resource(FriendsApi, "/api/user/friends")
    api.add_resource(FriendRequestApi, "/api/user/friend_request")
    api.add_resource(FriendRequestsApi, "/api/user/friend_requests")
    api.add_resource(UserSearchApi, "/api/user/search")
    api.add_resource(GetPlaceApi, "/api/place/<place_id>")
    api.add_resource(RatePlaceApi, "/api/place/rate")
    api.add_resource(RecommendationApi, "/api/recommendations")
