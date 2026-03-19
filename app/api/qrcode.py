from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.generated_models import Qrcodes as QRCode, Users # Import model
from app.schemas.qrcode import QRCodeCreate, QRCodeResponse, QRCodeUpdate
from app.core.utils import generate_short_code
from app.db.session import get_db
from app.api.auth import get_current_user

router = APIRouter(prefix="/qrcodes", tags=["QRCodes"])

@router.post("/", response_model=QRCodeResponse)
def create_qrcode(
        qr_in: QRCodeCreate,
        db: Session = Depends(get_db),
        current_user: Users = Depends(get_current_user)
):
    # 1. Sinh short_code độc nhất
    new_short_code = generate_short_code()
    while db.query(QRCode).filter(QRCode.short_code == new_short_code).first():
        new_short_code = generate_short_code() # Sinh lại nếu bị trùng

    # 2. Tạo record trong Database
    new_qr = QRCode(
        **qr_in.model_dump(),
        user_id=current_user.id,
        short_code=new_short_code
    )

    db.add(new_qr)
    db.commit()
    db.refresh(new_qr)

    return new_qr


@router.put("/{qrcode_id}", response_model=QRCodeResponse)
def update_qrcode(
    qrcode_id: int,
    qr_in: QRCodeUpdate,
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user),
):
    qrcode = (
        db.query(QRCode)
        .filter(QRCode.id == qrcode_id, QRCode.user_id == current_user.id)
        .first()
    )
    if not qrcode:
        raise HTTPException(status_code=404, detail="QRCode not found")

    update_data = qr_in.model_dump(exclude_unset=True, exclude_none=True)
    for field, value in update_data.items():
        setattr(qrcode, field, value)

    db.commit()
    db.refresh(qrcode)
    return qrcode


@router.delete("/{qrcode_id}")
def delete_qrcode(
    qrcode_id: int,
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user),
):
    qrcode = (
        db.query(QRCode)
        .filter(QRCode.id == qrcode_id, QRCode.user_id == current_user.id)
        .first()
    )
    if not qrcode:
        raise HTTPException(status_code=404, detail="QRCode not found")

    db.delete(qrcode)
    db.commit()
    return {"message": "QRCode deleted successfully"}

@router.get("/campaign/{campaign_id}", response_model=list[QRCodeResponse])
def get_qrcodes_by_campaign(
    campaign_id: int,
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user),
):
    return (
        db.query(QRCode)
        .filter(QRCode.campaign_id == campaign_id, QRCode.user_id == current_user.id)
        .all()
    )
