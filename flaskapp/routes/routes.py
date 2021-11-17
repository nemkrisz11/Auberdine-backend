from flaskapp.routes.index.index import IndexApi
from flaskapp.routes.user.login import LoginApi
from flaskapp.routes.user.register import RegisterApi


def initialize_routes(api):
    api.add_resource(RegisterApi, '/user/register')
    api.add_resource(LoginApi, '/user/login')
    api.add_resource(IndexApi, '/')
