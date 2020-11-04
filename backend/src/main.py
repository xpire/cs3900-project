from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware

from src.api.api import api_router
from src.core.config import settings
from src.schemas.response import Result, ResultException

app = FastAPI(title=settings.PROJECT_NAME)

# # Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGIN:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGIN,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router)
