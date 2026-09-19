from fastapi import FastAPI
# define .env file path and load environment variables
from dotenv import load_dotenv
load_dotenv(".env")

from routes import base
app = FastAPI()

app.include_router(base.base_router)