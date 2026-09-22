from fastapi import FastAPI, APIRouter, Depends, UploadFile, File, status
from fastapi.responses import JSONResponse
from helpers.config import get_settings, Settings
from controllers import DataController
from models import ResponseSignal

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["data", "api_v1"],
)


@data_router.post("/upload/{project_id}")
async def upload_file(project_id: str,
                    file: UploadFile = File(...),
                    app_settings: Settings = Depends(get_settings)):

    data_controller = DataController()

    is_valid, signal = data_controller.validate_file(file=file)

    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"signal": signal}
        )

    file_path, file_id = data_controller.generate_unique_filepath(
        orig_filename=file.filename, project_id=project_id
    )

    try:
        await data_controller.save_file(file=file, file_path=file_path)
    except Exception:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"signal": ResponseSignal.FILE_UPLOAD_FAILED.value}
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "signal": ResponseSignal.FILE_UPLOAD_SUCCESS.value,
            "file_id": file_id,
            "project_id": project_id,
        }
    )