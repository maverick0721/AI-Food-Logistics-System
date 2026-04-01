from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routers import order_router
from backend.routers import restaurant_router
from backend.routers import delivery_router
from backend.routers import recommendation_router
from backend.routers import metrics_router
from backend.routers import config_router
from backend.database.init_db import init_db


@asynccontextmanager
async def lifespan(_app: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(order_router.router)
app.include_router(restaurant_router.router)
app.include_router(delivery_router.router)
app.include_router(recommendation_router.router)
app.include_router(metrics_router.router)
app.include_router(config_router.router)


@app.get("/")

def root():

    return {"message": "AI Food Logistics API"}