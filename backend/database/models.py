from sqlalchemy import Column, Integer, String

from backend.database.db import Base


class OrderDB(Base):

    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer)

    restaurant_id = Column(Integer)

    item = Column(String)


class RestaurantDB(Base):

    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String)

    cuisine = Column(String)