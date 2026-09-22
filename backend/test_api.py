"""Smoke and validation tests. These run against a real MySQL instance:
the schema and the DECIMAL handling are part of what is being tested.
"""

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_health_reports_database_reachable():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "database": "reachable"}


def test_records_respects_limit():
    response = client.get("/records", params={"limit": 5})
    assert response.status_code == 200
    assert len(response.json()) <= 5


def test_records_rejects_out_of_range_pagination():
    assert client.get("/records", params={"limit": 999}).status_code == 422
    assert client.get("/records", params={"offset": -1}).status_code == 422


def test_records_unknown_team_is_empty_not_404():
    response = client.get("/records", params={"team": "NoSuchTeam"})
    assert response.status_code == 200
    assert response.json() == []


def test_summary_totals_are_positive():
    response = client.get("/summary")
    assert response.status_code == 200
    rows = response.json()
    assert rows, "expected seeded data"
    for row in rows:
        assert row["total_tokens"] > 0
        # cost is a string so money never passes through a float
        assert isinstance(row["total_cost"], str)


def test_top_users_is_sorted_descending():
    rows = client.get("/top-users", params={"limit": 5}).json()
    tokens = [row["total_tokens"] for row in rows]
    assert tokens == sorted(tokens, reverse=True)


def test_create_rejects_invalid_payloads():
    base = {
        "user_name": "Test",
        "team": "Analytics",
        "tool": "Cursor",
        "tokens": 10,
        "cost": "1.00",
        "used_on": "2026-09-21",
    }
    assert client.post("/records", json={**base, "tokens": -1}).status_code == 422
    assert client.post("/records", json={**base, "cost": "1.234"}).status_code == 422
    assert client.post("/records", json={**base, "used_on": "nope"}).status_code == 422
    assert client.post("/records", json={k: v for k, v in base.items() if k != "team"}).status_code == 422


def test_create_returns_201_and_persists():
    payload = {
        "user_name": "Pytest Person",
        "team": "Analytics",
        "tool": "Claude Code",
        "tokens": 4242,
        "cost": "0.99",
        "used_on": "2026-09-21",
    }
    created = client.post("/records", json=payload)
    assert created.status_code == 201

    body = created.json()
    assert body["id"] > 0
    assert body["cost"] == "0.99"

    listed = client.get("/records", params={"team": "Analytics", "limit": 50}).json()
    assert any(row["id"] == body["id"] for row in listed)
