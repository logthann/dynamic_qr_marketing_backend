from fastapi import FastAPI

from .api import router as api_router


def create_app() -> FastAPI:
    app = FastAPI(title="QR Marketing Backend")
    app.include_router(api_router, prefix="/api")
    return app
