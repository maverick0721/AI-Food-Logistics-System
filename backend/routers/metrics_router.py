from fastapi import APIRouter

from backend.services.metrics_service import get_dashboard_metrics


router = APIRouter()


@router.get("/metrics/dashboard")
def dashboard_metrics():
    return get_dashboard_metrics()
