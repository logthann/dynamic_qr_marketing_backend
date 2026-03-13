from pydantic import BaseModel
from typing import Optional
from datetime import date

class CampaignCreate(BaseModel):
    name: str
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    ga_measurement_id: Optional[str] = None

class CampaignResponse(CampaignCreate):
    id: int
    user_id: int
    status: str

    class Config:
        orm_mode = True