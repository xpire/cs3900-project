from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from backend.src.apis.api_stocks.api import stock_api_router
from backend.src.apis.api_user.api import user_api_router

from backend.src.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    # openapi_url = f"{settings.}/openapi.json"
)

# # Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGIN:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"], #[str(origin) for origin in settings.BACKEND_CORS_ORIGIN],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(stock_api_router)  # , prefix=settings.API_V1_STR)
app.include_router(user_api_router)  # , prefix=settings.API_V1_STR)
