from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.core.tenancy import get_session_maker_for_request
from app.models.petitions import Petition
from app.models.signatures import Signature
from app.models.campaigns import Campaign
from app.utils.filters import like

router = APIRouter(prefix="/search", tags=["Busca"])

def get_db(request: Request):
    SessionLocal = get_session_maker_for_request(request)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("")
def search(q: str, type: str = "petitions", limit: int = 10, db: Session = Depends(get_db)):
    if type == "petitions":
        return db.query(Petition).filter(Petition.title.ilike(like(q))).limit(limit).all()
    elif type == "signatures":
        return db.query(Signature).filter(Signature.name.ilike(like(q))).limit(limit).all()
    elif type == "campaigns":
        return db.query(Campaign).filter(Campaign.name.ilike(like(q))).limit(limit).all()
    return []
