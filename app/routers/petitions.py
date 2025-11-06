from fastapi import APIRouter, Depends, Request, HTTPException, Response
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.schemas.petitions import PetitionIn, PetitionOut
from app.models.petitions import Petition
from app.models.signatures import Signature
from app.services.csv_export import rows_to_csv_bytes
from app.services.analytics import petition_overview
from app.core.tenancy import get_session_maker_for_request
from app.utils.pagination import normalize_pagination

router = APIRouter(prefix="/petitions", tags=["Petições"])

def get_db(request: Request):
    SessionLocal = get_session_maker_for_request(request)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("", response_model=list[PetitionOut])
def list_petitions(limit: int = 50, offset: int = 0, db: Session = Depends(get_db)):
    l, o = normalize_pagination(limit, offset)
    return db.query(Petition).order_by(Petition.created_date.desc()).limit(l).offset(o).all()

@router.post("", response_model=PetitionOut)
def create_petition(payload: PetitionIn, db: Session = Depends(get_db)):
    item = Petition(**payload.dict())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@router.get("/{id}", response_model=PetitionOut)
def get_petition(id: str, db: Session = Depends(get_db)):
    item = db.get(Petition, id)
    if not item:
        raise HTTPException(404, "Petição não encontrada")
    return item

@router.put("/{id}", response_model=PetitionOut)
def update_petition(id: str, payload: PetitionIn, db: Session = Depends(get_db)):
    item = db.get(Petition, id)
    if not item:
        raise HTTPException(404, "Petição não encontrada")
    for k, v in payload.dict().items():
        setattr(item, k, v)
    db.commit()
    db.refresh(item)
    return item

@router.delete("/{id}")
def delete_petition(id: str, db: Session = Depends(get_db)):
    item = db.get(Petition, id)
    if not item:
        raise HTTPException(404, "Petição não encontrada")
    db.delete(item)
    db.commit()
    return {"ok": True}

@router.get("/slug/{slug}", response_model=PetitionOut)
def get_by_slug(slug: str, db: Session = Depends(get_db)):
    item = db.query(Petition).filter(Petition.slug == slug).first()
    if not item:
        raise HTTPException(404, "Petição não encontrada")
    return item

@router.get("/{id}/analytics")
def petition_analytics(id: str, db: Session = Depends(get_db)):
    data = petition_overview(db, id)
    if not data:
        raise HTTPException(404, "Dados não encontrados")
    return data

@router.get("/{id}/export-csv")
def export_signatures_csv(id: str, db: Session = Depends(get_db)):
    rows = db.query(Signature).filter(Signature.petition_id == id).all()
    serial = []
    for s in rows:
        serial.append({
            "id": str(s.id),
            "petition_id": str(s.petition_id),
            "name": s.name,
            "email": s.email,
            "city": s.city or "",
            "state": s.state or "",
            "created_date": s.created_date.isoformat() if s.created_date else ""
        })
    csv_bytes = rows_to_csv_bytes(serial)
    return Response(content=csv_bytes, media_type="text/csv",
                    headers={"Content-Disposition": f"attachment; filename=signatures_{id}.csv"})
