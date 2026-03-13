from fastapi.testclient import TestClient

from backend.main import app
from backend.routers import delivery_router, metrics_router, order_router, recommendation_router, restaurant_router


client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "AI Food Logistics API"}


def test_restaurants_endpoints(monkeypatch):
    monkeypatch.setattr(
        restaurant_router,
        "add_restaurant",
        lambda restaurant: {"id": 1, "name": restaurant.name, "cuisine": restaurant.cuisine},
    )
    monkeypatch.setattr(
        restaurant_router,
        "list_restaurants",
        lambda: [{"id": 1, "name": "Demo Kitchen", "cuisine": "Indian"}],
    )

    create_res = client.post("/restaurants", json={"name": "Demo Kitchen", "cuisine": "Indian"})
    assert create_res.status_code == 200
    assert create_res.json()["name"] == "Demo Kitchen"

    list_res = client.get("/restaurants")
    assert list_res.status_code == 200
    assert isinstance(list_res.json(), list)


def test_orders_endpoints(monkeypatch):
    monkeypatch.setattr(
        order_router,
        "create_order",
        lambda order: {
            "id": 101,
            "user_id": order.user_id,
            "restaurant_id": order.restaurant_id,
            "item": order.item,
        },
    )
    monkeypatch.setattr(
        order_router,
        "list_orders",
        lambda: [{"id": 101, "user_id": 1, "restaurant_id": 1, "item": "burger"}],
    )

    create_res = client.post("/orders", json={"user_id": 1, "restaurant_id": 1, "item": "burger"})
    assert create_res.status_code == 200
    assert create_res.json()["item"] == "burger"

    list_res = client.get("/orders")
    assert list_res.status_code == 200
    assert isinstance(list_res.json(), list)


def test_recommend_endpoint(monkeypatch):
    monkeypatch.setattr(
        recommendation_router,
        "recommend",
        lambda user_id, restaurant_id: {
            "user_id": user_id,
            "restaurant_id": restaurant_id,
            "score": 0.42,
        },
    )

    response = client.get("/recommend", params={"user_id": 1, "restaurant_id": 2})
    assert response.status_code == 200
    assert response.json()["score"] == 0.42


def test_dispatch_endpoint(monkeypatch):
    monkeypatch.setattr(delivery_router, "assign_driver", lambda order_id: order_id % 20)

    response = client.post("/dispatch/7")
    assert response.status_code == 200
    assert response.json() == 7


def test_dashboard_metrics_endpoint(monkeypatch):
    monkeypatch.setattr(
        metrics_router,
        "get_dashboard_metrics",
        lambda: {
            "uptime_pct": 99.9,
            "active_zones": 4,
            "avg_eta_minutes": 17.5,
            "stream_lag_ms": 32,
        },
    )

    response = client.get("/metrics/dashboard")
    assert response.status_code == 200
    assert response.json()["active_zones"] == 4


def test_create_order_validation_error():
    response = client.post("/orders", json={"user_id": 1, "restaurant_id": 1})
    assert response.status_code == 422


def test_recommend_validation_error_missing_query_params():
    response = client.get("/recommend")
    assert response.status_code == 422


def test_dispatch_validation_error_invalid_order_id_type():
    response = client.post("/dispatch/not-an-int")
    assert response.status_code == 422


def test_orders_internal_error_response(monkeypatch):
    def _raise_error(_order):
        raise RuntimeError("db unavailable")

    monkeypatch.setattr(order_router, "create_order", _raise_error)
    local_client = TestClient(app, raise_server_exceptions=False)
    response = local_client.post("/orders", json={"user_id": 1, "restaurant_id": 1, "item": "burger"})
    assert response.status_code == 500
