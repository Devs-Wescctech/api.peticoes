from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_, desc
from app.schemas.signatures import SignatureIn, SignatureOut
from app.models.signatures import Signature
from app.utils.pagination import normalize_pagination
from app.utils.filters import like
from app.services.csv_export import rows_to_csv_bytes
from fastapi import Response

router = APIRouter(prefix="/signatures", tags=["Assinaturas"])

from app.core.tenancy import get_session_maker_for_request
def get_db(request: Request):
    SessionLocal = get_session_maker_for_request(request)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("", response_model=list[SignatureOut])
def list_signatures(petition_id: str | None = None,
                    city: str | None = None,
                    state: str | None = None,
                    date_from: str | None = None,
                    date_to: str | None = None,
                    limit: int = 50,
                    offset: int = 0,
                    sort: str | None = None,
                    db: Session = Depends(get_db)):
    l, o = normalize_pagination(limit, offset)
    q = db.query(Signature)
    if petition_id:
        q = q.filter(Signature.petition_id == petition_id)
    if city:
        q = q.filter(Signature.city.ilike(like(city)))
    if state:
        q = q.filter(Signature.state.ilike(like(state)))
    if date_from:
        q = q.filter(Signature.created_date >= date_from)
    if date_to:
        q = q.filter(Signature.created_date <= date_to)
    if sort == "-created_date":
        q = q.order_by(Signature.created_date.desc())
    else:
        q = q.order_by(Signature.created_date.asc())
    return q.limit(l).offset(o).all()

@router.post("", response_model=SignatureOut)
def create_signature(payload: SignatureIn, request: Request, db: Session = Depends(get_db)):
    ip = request.client.host if request.client else None
    ua = request.headers.get("user-agent", "")
    item = Signature(**payload.dict(), ip_address=ip, user_agent=ua)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@router.get("/{id}", response_model=SignatureOut)
def get_signature(id: str, db: Session = Depends(get_db)):
    item = db.get(Signature, id)
    if not item:
        raise HTTPException(404, "Assinatura não encontrada")
    return item

@router.delete("/{id}")
def delete_signature(id: str, db: Session = Depends(get_db)):
    item = db.get(Signature, id)
    if not item:
        raise HTTPException(404, "Assinatura não encontrada")
    db.delete(item)
    db.commit()
    return {"ok": True}

@router.post("/import")
def import_signatures(items: list[SignatureIn], db: Session = Depends(get_db)):
    created = 0
    for payload in items:
        s = Signature(**payload.dict())
        db.add(s)
        created += 1
    db.commit()
    return {"imported": created}

@router.get("/export-csv")
def export_csv(petition_id: str | None = None, db: Session = Depends(get_db)):
    q = db.query(Signature)
    if petition_id:
        q = q.filter(Signature.petition_id == petition_id)
    rows = q.all()
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
                    headers={"Content-Disposition": "attachment; filename=signatures.csv"})
