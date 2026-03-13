from fastapi import FastAPI
    return app
    app.include_router(api_router, prefix="/api")
    app = FastAPI(title="QR Marketing Backend")
    """Create and configure the FastAPI application."""
def create_app() -> FastAPI:


from .api import router as api_router

