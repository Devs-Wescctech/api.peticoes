from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.schemas.campaign_logs import CampaignLogIn, CampaignLogOut
from app.models.campaign_logs import CampaignLog
from app.core.tenancy import get_session_maker_for_request

router = APIRouter(prefix="/campaign-logs", tags=["Logs de Campanha"])

def get_db(request: Request):
    SessionLocal = get_session_maker_for_request(request)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("", response_model=list[CampaignLogOut])
def list_logs(campaign_id: str | None = None, status: str | None = None, limit: int = 100, offset: int = 0,
              db: Session = Depends(get_db)):
    q = db.query(CampaignLog)
    if campaign_id:
        q = q.filter(CampaignLog.campaign_id == campaign_id)
    if status:
        q = q.filter(CampaignLog.status == status)
    return q.order_by(CampaignLog.sent_at.desc()).limit(limit).offset(offset).all()

@router.post("", response_model=CampaignLogOut)
def create_log(payload: CampaignLogIn, db: Session = Depends(get_db)):
    item = CampaignLog(**payload.dict())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@router.get("/{id}", response_model=CampaignLogOut)
def get_log(id: str, db: Session = Depends(get_db)):
    item = db.get(CampaignLog, id)
    return item

@router.get("/campaign/{id}")
def logs_by_campaign(id: str, db: Session = Depends(get_db)):
    return db.query(CampaignLog).filter(CampaignLog.campaign_id == id).order_by(CampaignLog.sent_at.desc()).all()

@router.get("/campaign/{id}/errors")
def logs_errors_by_campaign(id: str, db: Session = Depends(get_db)):
    return db.query(CampaignLog).filter(CampaignLog.campaign_id == id, CampaignLog.status == "error").all()
