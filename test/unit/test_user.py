import pytest
from flaskapp.app import create_app
from mongoinit.init_flaskdb import init


@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        with app.app_context():
            init(app["MONGO_URI"])
        yield client


def test_shiny_case():
    assert True is bool([5])