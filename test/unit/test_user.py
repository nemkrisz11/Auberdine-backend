from flask import request
import pytest
from fixtures import client
from flaskapp.models.user import User


def test_get_user(client):
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

    assert resp.status_code == 200
    assert resp.is_json
    assert resp.json == {}


def test_valid_login(client):
    resp = client.post("/user/login",
                       data={"email": "goldschmidt@iit.bme.hu",
                             "password": "12345678"})
    assert resp.status_code == 200
    assert resp.is_json
    assert len(resp.headers["Authorization"]) > 20  # TODO: more sensible token check




def test_invalid_login(client):
    resp = client.post("/user/login",
                       data={"email": "goldschmidt@iit.bme.hu",
                             "password": "qwertyasd"})
    assert resp.status_code == 200
    assert resp.is_json
    assert "access_token" not in resp.json
    assert "email" not in resp.json
    assert "password" in resp.json
