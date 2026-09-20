from .BaseController import BaseController
from fastapi import UploadFile

class DataController(BaseController):
    def __init__(self):
        super().__init__()
    
    def validate_file(self, file: UploadFile):
        # Validate file extension
        if not self.is_allowed_extension(file.content_type):
            raise ValueError(f"File extension not allowed. Allowed extensions: {self.settings.FILE_ALLOWED_EXTENSIONS}")
        
        # Validate file size
        if not self.is_allowed_size(file):
            raise ValueError(f"File size exceeds the maximum limit of {self.settings.FILE_MAX_SIZE_MB} MB.")

    def is_allowed_extension(self, content_type: str) -> bool:
        return content_type in self.settings.FILE_ALLOWED_EXTENSIONS

    def is_allowed_size(self, file: UploadFile) -> bool:
        max_size_bytes = self.settings.FILE_MAX_SIZE_MB * 1024 * 1024
        return file.size is not None and file.size <= max_size_bytes
