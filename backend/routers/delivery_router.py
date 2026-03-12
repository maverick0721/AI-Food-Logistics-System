from fastapi import APIRouter

from backend.services.delivery_service import assign_driver


router = APIRouter()


@router.post("/dispatch/{order_id}")

def dispatch(order_id: int):

    return assign_driver(order_id)