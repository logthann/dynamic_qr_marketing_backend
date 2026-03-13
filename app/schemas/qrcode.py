from pydantic import BaseModel
from typing import Optional, Dict, Any

class QRCodeCreate(BaseModel):
    name: str
    campaign_id: Optional[int] = None
    destination_url: str
    qr_type: Optional[str] = "url"
    design_config: Optional[Dict[str, Any]] = None # Chứa JSON cấu hình màu sắc, logo

class QRCodeResponse(QRCodeCreate):
    id: int
    user_id: int
    short_code: str
    status: str

    class Config:
        orm_mode = True