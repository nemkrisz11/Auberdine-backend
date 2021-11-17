import pytest
from fixtures import client
from flask import request


def test_debug_places(client):
    rv = client.get("/place/debug_places")
    assert "Bivalybasznád" in rv.get_data(as_text=True)


