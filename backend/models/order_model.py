from pydantic import BaseModel


class Order(BaseModel):

    user_id: int
    restaurant_id: int
    item: str