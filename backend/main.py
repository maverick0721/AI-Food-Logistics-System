from fastapi import FastAPI

from backend.routers import order_router
from backend.routers import restaurant_router
from backend.routers import delivery_router
from backend.routers import recommendation_router


app = FastAPI()

app.include_router(order_router.router)
app.include_router(restaurant_router.router)
app.include_router(delivery_router.router)
app.include_router(recommendation_router.router)


@app.get("/")

def root():

    return {"message": "AI Food Logistics API"}