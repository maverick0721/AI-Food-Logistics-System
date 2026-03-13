from backend.database.db import SessionLocal
from backend.database.models import OrderDB, RestaurantDB


def get_dashboard_metrics():
    db = SessionLocal()
    try:
        orders = db.query(OrderDB).all()
        restaurants = db.query(RestaurantDB).all()

        orders_count = len(orders)
        restaurants_count = len(restaurants)

        if orders_count:
            avg_eta_minutes = round(
                sum(12 + (order.restaurant_id % 7) for order in orders) / orders_count,
                1,
            )
        else:
            avg_eta_minutes = 0.0

        stream_lag_ms = min(350, max(12, orders_count * 7 + restaurants_count * 3))

        return {
            "uptime_pct": 99.9,
            "active_zones": restaurants_count,
            "avg_eta_minutes": avg_eta_minutes,
            "stream_lag_ms": stream_lag_ms,
        }
    finally:
        db.close()
