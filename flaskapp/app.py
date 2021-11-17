import os
from flask import Flask, jsonify, Blueprint
from routes import friend_request, place, recommendation, user
from flask_jwt_extended import JWTManager
from mongoengine import connect
import datetime
import redis

bp = Blueprint("main", __name__)

TOKEN_EXPIRES = datetime.timedelta(minutes=30)
jwt = JWTManager()
jwt_redis_blocklist = redis.StrictRedis(
    host="localhost", port=6379, db=0, decode_responses=True
)


@bp.route('/')
def index():
    return jsonify(
        status=True,
        message='Welcome to the Auberdine Flask application!'
    )

# Callback function to check if a JWT exists in the redis blocklist
@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    token_in_redis = jwt_redis_blocklist.get(jti)
    return token_in_redis is not None


def create_app():
    application = Flask(__name__)
    application.config["MONGO_URI"] = 'mongodb://' + os.environ['MONGODB_USERNAME'] + ':' + os.environ[
        'MONGODB_PASSWORD'] + '@' + os.environ['MONGODB_HOSTNAME'] + ':' + os.environ['MONGODB_PORT'] + '/' + \
        os.environ['MONGODB_DATABASE']

    application.config["JWT_SECRET"] = "WpihOCz6HB6DgotdtmMabe7GJYLUIpWdAbNsK7bj4FgzWrFCrAOojog4g2sI3c4"
    application.config["JWT_ACCESS_TOKEN_EXPIRES"] = TOKEN_EXPIRES

    jwt.init_app(application)

    connect(host=application.config["MONGO_URI"])

    modules = [friend_request, place, recommendation, user.login, user.logout, user.register]
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
