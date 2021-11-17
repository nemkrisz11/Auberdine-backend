import os
from flask import Flask, jsonify, Blueprint
from flask_restful import Api, Resource
from flaskapp.routes.routes import initialize_routes
from flask_jwt_extended import JWTManager, jwt_required
from mongoengine import connect
import datetime

bp = Blueprint("main", __name__)

TOKEN_EXPIRES = datetime.timedelta(hours=6)
jwt = JWTManager()


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

    # TODO: CORS?

    return app


# if started directly, run with this config, won't be executed with wsgi
if __name__ == "__main__":
    app = create_app()
    ENV_DEBUG = bool(os.environ.get("APPLICATION_DEBUG", True))
    ENV_PORT = os.environ.get("APPLICATION_PORT", 5000)
    app.run(host='0.0.0.0', port=ENV_PORT, debug=ENV_DEBUG)
