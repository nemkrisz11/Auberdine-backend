from pymongo import MongoClient
from pathlib import Path
import os
import subprocess


def init(mongo_uri):
    """Initialize the mongodb for testing

    Params
    ------
    mongo_uri: URI of the mongodb to connect to
    """

    client = MongoClient(mongo_uri)
    db = client.flaskdb
    collections = ["users", "places", "reviews"]
    for coll in collections:
        db.drop_collection(coll)

    script_dir = Path(__file__).parent.absolute()
    initscript = os.path.join(script_dir, "init_flaskdb.js")
    subprocess.run(["mongo", mongo_uri, initscript])
