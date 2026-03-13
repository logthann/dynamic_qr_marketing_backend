from fastapi import APIRouter

router = APIRouter()


@router.get("/health", tags=["Health"])
async def health() -> dict:
    """Simple health endpoint."""
    return {"status": "ok", "service": "qr_marketing_backend"}

