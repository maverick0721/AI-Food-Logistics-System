import os
from pathlib import Path

from fastapi import APIRouter, HTTPException


router = APIRouter()


def _token_from_env_file():
    env_path = Path(__file__).resolve().parents[2] / ".env"
    if not env_path.exists():
        return ""

    for line in env_path.read_text(encoding="utf-8").splitlines():
        if not line or line.strip().startswith("#"):
            continue
        if line.startswith("REACT_APP_MAPBOX_TOKEN="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    return ""


@router.get("/config/mapbox-token")
def get_mapbox_token():
    token = (os.getenv("REACT_APP_MAPBOX_TOKEN") or "").strip()
    if not token:
        token = _token_from_env_file()

    if not token:
        raise HTTPException(status_code=404, detail="Mapbox token not configured")

    return {"token": token}
