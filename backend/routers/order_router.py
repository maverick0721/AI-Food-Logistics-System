from fastapi import APIRouter

from backend.models.order_model import Order
from backend.services.order_service import create_order, list_orders


router = APIRouter()


@router.post("/orders")

def create(order: Order):

    return create_order(order)


@router.get("/orders")

def get_orders():

    return list_orders()