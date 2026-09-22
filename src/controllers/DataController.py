import os
import re
from uuid import uuid4

import aiofiles
from fastapi import UploadFile

from .BaseController import BaseController
from models import ResponseSignal

class DataController(BaseController):
    def __init__(self):
        super().__init__()

    def validate_file(self, file: UploadFile) -> tuple[bool, str]:
        # Validate file extension
        if not self.is_allowed_extension(file.content_type):
            return False, ResponseSignal.FILE_TYPE_NOT_SUPPORTED.value

        # Validate file size
        if not self.is_allowed_size(file):
            return False, ResponseSignal.FILE_SIZE_EXCEEDED.value

        return True, ResponseSignal.FILE_VALIDATION_SUCCESS.value

    def is_allowed_extension(self, content_type: str) -> bool:
        return content_type in self.settings.FILE_ALLOWED_EXTENSIONS

    def is_allowed_size(self, file: UploadFile) -> bool:
        max_size_bytes = self.settings.FILE_MAX_SIZE_MB * 1024 * 1024
        return file.size is not None and file.size <= max_size_bytes

    def generate_unique_filepath(self, orig_filename: str, project_id: str) -> tuple[str, str]:
        cleaned_filename = self.get_clean_filename(orig_filename)
        new_filename = f"{uuid4().hex}_{cleaned_filename}"
        project_path = self.get_project_path(project_id=project_id)
        new_filepath = os.path.join(project_path, new_filename)
        return new_filepath, new_filename

    def get_clean_filename(self, orig_filename: str) -> str:
        return re.sub(r"[^\w.]", "_", orig_filename.strip())

    async def save_file(self, file: UploadFile, file_path: str) -> None:
        chunk_size = self.settings.FILE_UPLOAD_CHUNK_SIZE_KB * 1024
        async with aiofiles.open(file_path, "wb") as f:
            while chunk := await file.read(chunk_size):
                await f.write(chunk)
