import os
from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from mongoengine import connect
from flaskapp.routes.routes import initialize_routes
from flaskapp.models import user, place, review
from flaskapp.authorization import jwt, TOKEN_EXPIRES
import logging


def create_app():
    app = Flask(__name__)
    app.config["MONGO_URI"] = 'mongodb://' + os.environ['MONGODB_USERNAME'] + ':' + os.environ[
        'MONGODB_PASSWORD'] + '@' + os.environ['MONGODB_HOSTNAME'] + ':' + os.environ['MONGODB_PORT'] + '/' + \
        os.environ['MONGODB_DATABASE']

    app.config["JWT_SECRET_KEY"] = "WpihOCz6HB6DgotdtmMabe7GJYLUIpWdAbNsK7bj4FgzWrFCrAOojog4g2sI3c4"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = TOKEN_EXPIRES
    app.config["PROPAGATE_EXCEPTIONS"] = True

    logging.basicConfig(filename='/tmp/debug.log', level=logging.DEBUG)

    jwt.init_app(app)

    connect(host=app.config["MONGO_URI"])

    api = Api(app)
    initialize_routes(api)

    # Initialize collections
    for cl in [user.User, place.Place, review.Review]:
        cl.ensure_indexes()

    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    return app


# if started directly, run with this config, won't be executed with wsgi
if __name__ == "__main__":
    app = create_app()
    ENV_DEBUG = bool(os.environ.get("APPLICATION_DEBUG", True))
    ENV_PORT = os.environ.get("APPLICATION_PORT", 5000)
    app.run(host='0.0.0.0', port=ENV_PORT, debug=ENV_DEBUG)
