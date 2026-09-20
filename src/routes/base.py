from fastapi import FastAPI, APIRouter
import os

base_router = APIRouter(
    prefix="/api/v1",
    tags=["Base"],
)

@base_router.get("/")
async def welcome_message():
    app_name = os.getenv("APP_NAME")
    app_version = os.getenv("APP_VERSION")

    return {
        "App_name": app_name,
        "App_version": app_version,
        "status": "healthy"
    }