from flask_jwt_extended import JWTManager
from flaskapp.models.user import User
import redis
import datetime

TOKEN_EXPIRES = datetime.timedelta(hours=6)

jwt = JWTManager()

# Setup our redis connection for storing the blocklisted tokens. You will probably
# want your redis instance configured to persist data to disk, so that a restart
# does not cause your application to forget that a JWT was revoked.
jwt_redis_blocklist = redis.StrictRedis(
    host="redis", port=6379, db=0, decode_responses=True
)


@jwt.user_identity_loader
def user_identity_lookup(user):
    """
    Register a callback function that takes whatever object is passed in as the
    identity when creating JWTs and converts it to a JSON serializable format.
    """
    return str(user.id)


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    """
    Register a callback function that loads a user from your database whenever
    a protected route is accessed. This should return any python object on a
    successful lookup, or None if the lookup failed for any reason (for example
    if the user has been deleted from the database).
    """
    identity = jwt_data["sub"]
    return User.objects.get(id=identity)


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(_jwt_header, jwt_payload):
    """
    Callback function to check if a JWT exists in the redis blocklist
    """
    jti = jwt_payload["jti"]
    token_in_redis = jwt_redis_blocklist.get(jti)
    return token_in_redis is not None
