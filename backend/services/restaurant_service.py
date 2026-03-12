from backend.database.db import SessionLocal
from backend.database.models import RestaurantDB


def add_restaurant(restaurant):

    db = SessionLocal()

    db_restaurant = RestaurantDB(

        name=restaurant.name,
        cuisine=restaurant.cuisine

    )

    db.add(db_restaurant)

    db.commit()

    db.refresh(db_restaurant)

    db.close()

    return db_restaurant


def list_restaurants():

    db = SessionLocal()

    restaurants = db.query(RestaurantDB).all()

    db.close()

    return restaurants