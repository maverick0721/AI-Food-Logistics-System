from pathlib import Path

import requests

from backend.database.db import SessionLocal, engine
from backend.database.models import Base, RestaurantDB
from utils.config import load_config


def _get_city_from_config():
    config_path = Path(__file__).resolve().parents[2] / "configs" / "settings.yaml"
    if not config_path.exists():
        return "Local"

    try:
        config = load_config(config_path)
        return str(config.get("city", "Local")).strip() or "Local"
    except Exception:
        return "Local"


def _default_restaurants_for_city(city):
    return [
        (f"{city} Central Kitchen", "Multi-cuisine"),
        (f"{city} Spice Corner", "Indian"),
        (f"{city} Green Bowl", "Healthy"),
    ]


def _get_runtime_location():
    try:
        res = requests.get(
            "http://ip-api.com/json/?fields=status,city,lat,lon",
            timeout=1.5,
        )
        data = res.json() if res.ok else {}
        if data.get("status") == "success" and data.get("lat") is not None and data.get("lon") is not None:
            return {
                "city": (data.get("city") or "").strip() or "Local",
                "lat": float(data["lat"]),
                "lon": float(data["lon"]),
            }
    except Exception:
        pass
    return None


def _fetch_nearby_restaurants(lat, lon, limit=8):
    query = f"""
    [out:json][timeout:10];
    (
      node[\"amenity\"=\"restaurant\"](around:5000,{lat},{lon});
      way[\"amenity\"=\"restaurant\"](around:5000,{lat},{lon});
      relation[\"amenity\"=\"restaurant\"](around:5000,{lat},{lon});
    );
    out center tags;
    """

    try:
        res = requests.post(
            "https://overpass-api.de/api/interpreter",
            data={"data": query},
            timeout=3.0,
        )
        if not res.ok:
            return []

        data = res.json()
        elements = data.get("elements", [])
        results = []
        seen = set()

        for elem in elements:
            tags = elem.get("tags", {})
            name = (tags.get("name") or "").strip()
            if not name:
                continue
            if name.lower() in seen:
                continue

            cuisine = (tags.get("cuisine") or "Local").strip()
            if ";" in cuisine:
                cuisine = cuisine.split(";", 1)[0].strip()
            if cuisine:
                cuisine = cuisine.replace("_", " ").title()
            else:
                cuisine = "Local"

            seen.add(name.lower())
            results.append((name, cuisine))

            if len(results) >= limit:
                break

        return results
    except Exception:
        return []


def _resolve_seed_restaurants():
    runtime = _get_runtime_location()
    if runtime:
        nearby = _fetch_nearby_restaurants(runtime["lat"], runtime["lon"]) 
        if nearby:
            return nearby
        return _default_restaurants_for_city(runtime["city"])

    return _default_restaurants_for_city(_get_city_from_config())


def init_db():

    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        if db.query(RestaurantDB).count() == 0:
            db.add_all(
                [
                    RestaurantDB(name=name, cuisine=cuisine)
                    for name, cuisine in _resolve_seed_restaurants()
                ]
            )
            db.commit()
    finally:
        db.close()


if __name__ == "__main__":

    init_db()

    print("Database tables created")