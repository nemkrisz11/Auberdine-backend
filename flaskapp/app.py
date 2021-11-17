import os
from flask import Flask, jsonify, Blueprint
from flaskapp.routes import friend_request, place, recommendation
from flaskapp.routes.user import login, register
from flask_jwt_extended import JWTManager, jwt_required
from mongoengine import connect
import datetime

bp = Blueprint("main", __name__)

TOKEN_EXPIRES = datetime.timedelta(hours=6)
jwt = JWTManager()


@bp.route('/')
@jwt_required()
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

    application.config["JWT_SECRET_KEY"] = "WpihOCz6HB6DgotdtmMabe7GJYLUIpWdAbNsK7bj4FgzWrFCrAOojog4g2sI3c4"
    application.config["JWT_ACCESS_TOKEN_EXPIRES"] = TOKEN_EXPIRES

    jwt.init_app(application)

    connect(host=application.config["MONGO_URI"])

    modules = [friend_request, place, recommendation, login, register]
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
