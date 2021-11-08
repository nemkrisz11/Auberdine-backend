import os
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo

application = Flask(__name__)

application.config["MONGO_URI"] = 'mongodb://' + os.environ['MONGODB_USERNAME'] + ':' + os.environ[
    'MONGODB_PASSWORD'] + '@' + os.environ['MONGODB_HOSTNAME'] + ':27017/' + os.environ['MONGODB_DATABASE']

mongo = PyMongo(application)
db = mongo.db


@application.route('/')
def index():
    return jsonify(
        status=True,
        message='Welcome to the Aubergine Flask app!'
    )


if __name__ == "__main__":
    ENV_DEBUG = os.environ.get("APP_DEBUG", True)
    ENV_PORT = os.environ.get("APP_PORT", 5000)

    application.run(host='0.0.0.0', port=ENV_PORT, debug=ENV_DEBUG)
