from pymongo import MongoClient


def init(mongo_uri):
    """Initialize the mongodb for testing

    Params
    ------
    mongo_uri: URI of the mongodb to connect to
    """

    client = MongoClient(mongo_uri)
    db = client.flaskdb

    file = open("init_flaskdb.js", "r")
    db.eval(file.read())
