import os
from flask import Flask
from flask_restful import Api
from flaskapp.routes.routes import initialize_routes
# from flask_jwt_extended import JWTManager
from mongoengine import connect
import datetime

# from flaskapp.models.user import User
from flaskapp.authorization import jwt

TOKEN_EXPIRES = datetime.timedelta(hours=6)
# jwt = JWTManager()
#
#
# # Register a callback function that takes whatever object is passed in as the
# # identity when creating JWTs and converts it to a JSON serializable format.
# @jwt.user_identity_loader
# def user_identity_lookup(user):
#     return user.id
#
#
# # Register a callback function that loads a user from your database whenever
# # a protected route is accessed. This should return any python object on a
# # successful lookup, or None if the lookup failed for any reason (for example
# # if the user has been deleted from the database).
# @jwt.user_lookup_loader
# def user_lookup_callback(_jwt_header, jwt_data):
#     identity = jwt_data["sub"]
#     return User.objects.get(id=identity)


def create_app():
    app = Flask(__name__)
    app.config["MONGO_URI"] = 'mongodb://' + os.environ['MONGODB_USERNAME'] + ':' + os.environ[
        'MONGODB_PASSWORD'] + '@' + os.environ['MONGODB_HOSTNAME'] + ':' + os.environ['MONGODB_PORT'] + '/' + \
        os.environ['MONGODB_DATABASE']

    app.config["JWT_SECRET_KEY"] = "WpihOCz6HB6DgotdtmMabe7GJYLUIpWdAbNsK7bj4FgzWrFCrAOojog4g2sI3c4"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = TOKEN_EXPIRES

    jwt.init_app(app)

    connect(host=app.config["MONGO_URI"])

    api = Api(app)
    initialize_routes(api)

    # TODO: CORS might be needed for Angular?

    return app


# if started directly, run with this config, won't be executed with wsgi
if __name__ == "__main__":
    app = create_app()
    ENV_DEBUG = bool(os.environ.get("APPLICATION_DEBUG", True))
    ENV_PORT = os.environ.get("APPLICATION_PORT", 5000)
    app.run(host='0.0.0.0', port=ENV_PORT, debug=ENV_DEBUG)
