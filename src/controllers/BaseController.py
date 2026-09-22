import os

from helpers.config import get_settings, Settings


class BaseController:
    def __init__(self):
        self.settings = get_settings()
        self.base_dir = os.path.dirname(os.path.dirname(__file__))
        self.files_dir = os.path.join(self.base_dir, "assets", "files")

    def get_project_path(self, project_id: str) -> str:
        project_dir = os.path.join(self.files_dir, project_id)
        os.makedirs(project_dir, exist_ok=True)
        return project_dir
