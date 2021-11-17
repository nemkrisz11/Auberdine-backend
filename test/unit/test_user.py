from flask import request
import pytest
from test_fixtures import client
from flaskapp.models.user import User


def test_shiny_case():
    assert True is bool([5])


def test_get_user(client):
    """Test for GET /user/{user_id} route

    """

    users = User.objects(name__contains="Goldschmidt")
    assert len(users) == 1
    user = users[0]
    assert "iit" in user.email
    #client.get("/user/{}".format(user._id))