# tests/test_server.py
import os
import sys

# Add project root (one level up) to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(__file__, "..", "..")))

from fastapi.testclient import TestClient
from deployment.server import app

client = TestClient(app)

def test_read_root():
    res = client.get("/")
    assert res.status_code == 200
    assert res.json() == {"message": "Welcome to the Insurance Fraud Detection API"}
