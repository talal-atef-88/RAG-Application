from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    APP_NAME: str 
    APP_VERSION: str
    OPENAI_API_KEY: str
    FILE_ALLOWED_EXTENSIONS: list[str]
    FILE_MAX_SIZE_MB: int
    FILE_UPLOAD_CHUNK_SIZE_KB: int
    
    class Config:
        env_file = ".env"

def get_settings():
    return Settings()