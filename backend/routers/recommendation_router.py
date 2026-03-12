from fastapi import APIRouter

from backend.services.recommendation_service import recommend


router = APIRouter()


@router.get("/recommend")

def get_recommendation(user_id: int, restaurant_id: int):

    return recommend(user_id, restaurant_id)