from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from backend.src.api.api import api_router

from backend.src.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME
)

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