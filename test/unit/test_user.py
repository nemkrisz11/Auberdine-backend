from flask import request
import pytest
from fixtures import client
from flaskapp.models.user import User


def test_shiny_case():
    assert True is bool([5])


def test_users_exist(client):
    """Test for GET /user/{user_id} route

    """

    users = User.objects(name__contains="Goldschmidt")
    assert len(users) == 1
    user = users[0]
    assert "iit" in user.email

    users = User.objects()
    assert len(users) >= 6
    #client.get("/user/{}".format(user._id))


def test_valid_register(client):
    resp = client.post("/user/register",
                data={"name": "thisisauniqueuser34958",
                      "password": "12345678",
                      "confirm": "12345678",
                      "email": "uniqueemail53498@a.b"
                      })
    result = resp.json
    assert resp.status_code == 200
    assert len(result.keys()) == 3
    assert result["namevalid"] is True
    assert result["emailvalid"] is True
    assert result["passwordvalid"] is True


def test_valid_login(client):
    resp = client.post("/user/login",
                       data={"email": "goldschmidt@iit.bme.hu",
                             "password": "12345678"})
    result = resp.json
    assert resp.status_code == 200
    assert "access_token" in result
