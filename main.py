from fastapi import FastAPI
from app.api import auth

def create_app() -> FastAPI:
    app = FastAPI(title="Dynamic QR Marketing Backend")

    @app.get("/health")
    def health_check():
        return {"status": "ok"}

    app.include_router(auth.router)
    return app

app = create_app()