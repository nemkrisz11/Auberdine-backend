import pytest
from flaskapp.app import *
from mongoinit.init_flaskdb import init



@pytest.fixture
def client():
    """Creates a test client for the application.
    Supports standard werkzeug stuff, e.g.:
    https://werkzeug.palletsprojects.com/en/2.0.x/test/
    """
    app = create_app()
    with app.test_client() as client:
        with app.app_context():
            init(app.config["MONGO_URI"])
        yield client
