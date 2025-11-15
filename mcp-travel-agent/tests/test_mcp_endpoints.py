# tests/test_mcp_endpoints.py
import pytest
from fastapi.testclient import TestClient
from mcp_server.app import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert "ok" in r.json()

def test_search_flights_found():
    payload = {"origin":"BOM","destination":"DXB","date":"2025-12-05","passengers":1}
    r = client.post("/search_flights", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert len(data) >= 1

def test_compare_fares_no_match():
    r = client.post("/compare_fares", json=["NO-FLIGHT"])
    assert r.status_code == 404
    assert r.json()["detail"] == "No matching flights for comparison"