import pytest
from flaskapp.app import *
from mongoinit.init_flaskdb import init


@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        with app.app_context():
            init(app.config["MONGO_URI"])
        yield client
