from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any

class QRCodeCreate(BaseModel):
    name: str
    campaign_id: Optional[int] = None
    destination_url: str
    qr_type: Optional[str] = "url"
    design_config: Optional[Dict[str, Any]] = None
    ga_measurement_id: Optional[str] = None
    utm_source: Optional[str] = None
    utm_medium: Optional[str] = None
    utm_campaign: Optional[str] = None


class QRCodeUpdate(BaseModel):
    name: Optional[str] = None
    campaign_id: Optional[int] = None
    destination_url: Optional[str] = None
    qr_type: Optional[str] = None
    design_config: Optional[Dict[str, Any]] = None
    ga_measurement_id: Optional[str] = None
    utm_source: Optional[str] = None
    utm_medium: Optional[str] = None
    utm_campaign: Optional[str] = None
    status: Optional[str] = None


class QRCodeResponse(QRCodeCreate):
    id: int
    user_id: int
    short_code: str
    status: str

    model_config = ConfigDict(from_attributes=True)
