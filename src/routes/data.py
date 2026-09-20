from fastapi import FastAPI, APIRouter, Depends, UploadFile, File, HTTPException, status
from helpers.config import get_settings, Settings
from controllers import DataController

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["data", "api_v1"],
)


@data_router.post("/upload/{project_id}")
async def upload_file(project_id: str,
                    file: UploadFile = File(...),
                    app_settings: Settings = Depends(get_settings)):
    try:
        DataController().validate_file(file=file)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return {
        "message": f"File '{file.filename}' uploaded successfully for project '{project_id}'."
    }