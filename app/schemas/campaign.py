from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date

class CampaignCreate(BaseModel):
    name: str
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    ga_measurement_id: Optional[str] = None


class CampaignUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    ga_measurement_id: Optional[str] = None
    status: Optional[str] = None


class CampaignResponse(CampaignCreate):
    id: int
    user_id: int
    status: str

    model_config = ConfigDict(from_attributes=True)
