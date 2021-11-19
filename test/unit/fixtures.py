"""Fixtures are methods that set up, and restore a context for the test case.
See: https://docs.pytest.org/en/6.2.x/fixture.html
"""

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


@pytest.fixture
def token(client, request):
    """Logs in the user with the email in pytest.mark.email, and
    yields an access token """

    rv = client.post("/user/login", data={
        "email": request.node.get_closest_marker("email").args[0],
        "password": request.node.get_closest_marker("password").args[0]
    })

    assert rv.is_json and rv.json == {}
    assert "Authorization" in rv.headers
    yield rv.headers["Authorization"]

    rv = client.delete("/user/logout", headers={"Authorization": "Bearer " + rv.headers["Authorization"]})
    assert rv.is_json and rv.json["msg"] == "ok"


