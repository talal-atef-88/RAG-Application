from fastapi import FastAPI, APIRouter, Depends
from helpers.config import get_settings, Settings


base_router = APIRouter(
    prefix="/api/v1",
    tags=["Base"],
)

@base_router.get("/")
async def welcome_message(app_seetings: Settings = Depends(get_settings)):
    
    app_name = app_seetings.APP_NAME
    app_version = app_seetings.APP_VERSION

    return {
        "App_name": app_name,
        "App_version": app_version,
        "status": "healthy"
    }