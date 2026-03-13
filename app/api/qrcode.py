from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.generated_models import Qrcodes as QRCode # Import model
from app.schemas.qrcode import QRCodeCreate, QRCodeResponse
from app.core.utils import generate_short_code
from app.db.session import get_db
from app.api.auth import get_current_user

router = APIRouter(prefix="/qrcodes", tags=["QRCodes"])

@router.post("/", response_model=QRCodeResponse)
def create_qrcode(
        qr_in: QRCodeCreate,
        db: Session = Depends(get_db),
        current_user_id: int = Depends(get_current_user)
):
    # 1. Sinh short_code độc nhất
    new_short_code = generate_short_code()
    while db.query(QRCode).filter(QRCode.short_code == new_short_code).first():
        new_short_code = generate_short_code() # Sinh lại nếu bị trùng

    # 2. Tạo record trong Database
    new_qr = QRCode(
        **qr_in.dict(),
        user_id=current_user_id,
        short_code=new_short_code
    )

    db.add(new_qr)
    db.commit()
    db.refresh(new_qr)

    return new_qr