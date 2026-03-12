from fastapi import APIRouter

from backend.models.restaurant_model import Restaurant
from backend.services.restaurant_service import add_restaurant, list_restaurants


router = APIRouter()


@router.post("/restaurants")

def create_restaurant(restaurant: Restaurant):

    return add_restaurant(restaurant)


@router.get("/restaurants")

def get_restaurants():

    return list_restaurants()