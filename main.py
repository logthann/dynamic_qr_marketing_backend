from fastapi import FastAPI
from app.api import auth, campaign, qrcode

def create_app() -> FastAPI:
    app = FastAPI(title="Dynamic QR Marketing Backend")

    @app.get("/health")
    def health_check():
        return {"status": "ok"}

    app.include_router(auth.router)
    app.include_router(campaign.router)
    app.include_router(qrcode.router)
    return app

app = create_app()