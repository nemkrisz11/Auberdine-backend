import os
from flask import Flask, request, jsonify, Blueprint
from routes import friend_request, place, recommendation, user
from mongoengine import connect


bp = Blueprint("main", __name__)


@bp.route('/')
def index():
    return jsonify(
        status=True,
        message='Welcome to the Auberdine Flask application!'
    )


def create_app():
    application = Flask(__name__)
    application.config["MONGO_URI"] = 'mongodb://' + os.environ['MONGODB_USERNAME'] + ':' + os.environ[
        'MONGODB_PASSWORD'] + '@' + os.environ['MONGODB_HOSTNAME'] + ':' + os.environ['MONGODB_PORT'] + '/' + \
        os.environ['MONGODB_DATABASE']

    connect(host=application.config["MONGO_URI"])

    modules = [friend_request, place, recommendation, user]
    application.register_blueprint(bp)
    for module in modules:
        application.register_blueprint(module.bp)

    return application


# if started directly, run with this config, won't be executed with wsgi
if __name__ == "__main__":
    app = create_app()
    ENV_DEBUG = bool(os.environ.get("APPLICATION_DEBUG", True))
    ENV_PORT = os.environ.get("APPLICATION_PORT", 5000)
    app.run(host='0.0.0.0', port=ENV_PORT, debug=ENV_DEBUG)




