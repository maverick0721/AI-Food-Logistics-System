from backend.database.db import SessionLocal
from backend.database.models import OrderDB


def create_order(order):

    db = SessionLocal()

    db_order = OrderDB(

        user_id=order.user_id,
        restaurant_id=order.restaurant_id,
        item=order.item

    )

    db.add(db_order)

    db.commit()

    db.refresh(db_order)

    db.close()

    return db_order


def list_orders():

    db = SessionLocal()

    orders = db.query(OrderDB).all()

    db.close()

    return orders