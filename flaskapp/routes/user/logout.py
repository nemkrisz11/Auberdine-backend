from flask import jsonify, Blueprint
from flask_jwt_extended import jwt_required, get_jwt

from flaskapp.app import jwt_redis_blocklist, TOKEN_EXPIRES

bp = Blueprint('logout_api', __name__, url_prefix="/user")


# Endpoint for revoking the current users access token. Save the JWTs unique
# identifier (jti) in redis. Also set a Time to Live (TTL)  when storing the JWT
# so that it will automatically be cleared out of redis after the token expires.
@bp.route("/logout", methods=['POST'])
@jwt_required()
def logout_user():
    jti = get_jwt()['jti']
    jwt_redis_blocklist.set(jti, "", ex=TOKEN_EXPIRES)
    return jsonify(msg="Access token revoked")
