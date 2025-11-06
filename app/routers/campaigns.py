from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from app.schemas.campaigns import CampaignIn, CampaignOut
from app.models.campaigns import Campaign
from app.core.tenancy import get_session_maker_for_request
from app.services.integrations import send_whatsapp, send_email

router = APIRouter(prefix="/campaigns", tags=["Campanhas"])

def get_db(request: Request):
    SessionLocal = get_session_maker_for_request(request)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("", response_model=list[CampaignOut])
def list_campaigns(type: str | None = None, status: str | None = None, petition_id: str | None = None,
                   db: Session = Depends(get_db)):
    q = db.query(Campaign)
    if type:
        q = q.filter(Campaign.type == type)
    if status:
        q = q.filter(Campaign.status == status)
    if petition_id:
        q = q.filter(Campaign.petition_id == petition_id)
    return q.order_by(Campaign.created_date.desc()).limit(200).all()

@router.post("", response_model=CampaignOut)
def create_campaign(payload: CampaignIn, db: Session = Depends(get_db)):
    item = Campaign(**payload.dict())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@router.get("/{id}", response_model=CampaignOut)
def get_campaign(id: str, db: Session = Depends(get_db)):
    item = db.get(Campaign, id)
    if not item:
        raise HTTPException(404, "Campanha não encontrada")
    return item

@router.put("/{id}", response_model=CampaignOut)
def update_campaign(id: str, payload: CampaignIn, db: Session = Depends(get_db)):
    item = db.get(Campaign, id)
    if not item:
        raise HTTPException(404, "Campanha não encontrada")
    for k, v in payload.dict().items():
        setattr(item, k, v)
    db.commit()
    db.refresh(item)
    return item

@router.delete("/{id}")
def delete_campaign(id: str, db: Session = Depends(get_db)):
    item = db.get(Campaign, id)
    if not item:
        raise HTTPException(404, "Campanha não encontrada")
    db.delete(item)
    db.commit()
    return {"ok": True}

@router.post("/{id}/send")
def start_sending(id: str, db: Session = Depends(get_db)):
    camp = db.get(Campaign, id)
    if not camp:
        raise HTTPException(404, "Campanha não encontrada")
    # Stub: apenas marca como "enviando"
    camp.status = "enviando"
    db.commit()
    return {"ok": True, "status": camp.status}

@router.post("/{id}/pause")
def pause_campaign(id: str, db: Session = Depends(get_db)):
    camp = db.get(Campaign, id)
    if not camp:
        raise HTTPException(404, "Campanha não encontrada")
    camp.status = "pausada"
    db.commit()
    return {"ok": True, "status": camp.status}

@router.post("/{id}/resume")
def resume_campaign(id: str, db: Session = Depends(get_db)):
    camp = db.get(Campaign, id)
    if not camp:
        raise HTTPException(404, "Campanha não encontrada")
    camp.status = "enviando"
    db.commit()
    return {"ok": True, "status": camp.status}

@router.get("/{id}/preview")
def preview_campaign(id: str, db: Session = Depends(get_db)):
    camp = db.get(Campaign, id)
    if not camp:
        raise HTTPException(404, "Campanha não encontrada")
    return {"message": camp.message, "subject": camp.subject}

@router.get("/{id}/recipients")
def recipients_campaign(id: str):
    # Stub: em produção, traga assinantes filtrados
    return {"recipients": []}
