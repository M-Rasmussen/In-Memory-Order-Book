import pytest
from fastapi.testclient import TestClient

from src.api import app, reset_engine_state


client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_api_state():
    reset_engine_state()


def test_health_check_returns_ok():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_submit_order_returns_created_order():
    response = client.post("/orders", json={"side": "buy", "price": 100, "quantity": 5})

    assert response.status_code == 201
    body = response.json()
    assert body["side"] == "buy"
    assert body["price"] == 100
    assert body["remaining_quantity"] == 5
    assert body["status"] == "open"


def test_order_matching_generates_trade():
    client.post("/orders", json={"side": "sell", "price": 99, "quantity": 3})
    response = client.post("/orders", json={"side": "buy", "price": 100, "quantity": 3})

    assert response.status_code == 201
    body = response.json()
    assert body["status"] == "filled"
    assert len(body["trades"]) == 1
    assert body["trades"][0]["price"] == 99
    assert body["trades"][0]["quantity"] == 3


def test_order_book_endpoint_returns_book_state():
    client.post("/orders", json={"side": "buy", "price": 100, "quantity": 5})
    response = client.get("/orderbook")

    assert response.status_code == 200
    body = response.json()
    assert body["top_of_book"]["best_bid"] == 100
    assert len(body["bids"]) == 1
    assert body["asks"] == []


def test_trades_endpoint_returns_recent_trades():
    client.post("/orders", json={"side": "sell", "price": 99, "quantity": 3})
    client.post("/orders", json={"side": "buy", "price": 100, "quantity": 3})

    response = client.get("/trades")

    assert response.status_code == 200
    trades = response.json()
    assert len(trades) == 1
    assert trades[0]["price"] == 99
