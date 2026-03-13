from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.auth import get_current_user
from app.db.session import get_db
from app.models.generated_models import Campaigns as Campaign, Users
from app.schemas.campaign import CampaignCreate, CampaignResponse

router = APIRouter(prefix="/campaigns", tags=["Campaigns"])


@router.post("/", response_model=CampaignResponse)
def create_campaign(
    campaign_in: CampaignCreate,
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user),
):
    new_campaign = Campaign(
        **campaign_in.dict(),
        user_id=current_user.id,
    )
    db.add(new_campaign)
    db.commit()
    db.refresh(new_campaign)
    return new_campaign


@router.get("/", response_model=list[CampaignResponse])
def get_my_campaigns(
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user),
):
    return db.query(Campaign).filter(Campaign.user_id == current_user.id).all()