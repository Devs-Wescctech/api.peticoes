from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from sqlalchemy import text as sqltext
from app.core.tenancy import get_session_maker_for_request

router = APIRouter(prefix="/analytics", tags=["Análises e Estatísticas"])

def get_db(request: Request):
    SessionLocal = get_session_maker_for_request(request)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/overview")
def overview(db: Session = Depends(get_db)):
    stats = {}
    stats["petitions"] = db.execute(sqltext("SELECT COUNT(*) FROM petitions")).scalar() or 0
    stats["signatures"] = db.execute(sqltext("SELECT COUNT(*) FROM signatures")).scalar() or 0
    stats["campaigns"] = db.execute(sqltext("SELECT COUNT(*) FROM campaigns")).scalar() or 0
    return stats

@router.get("/petitions")
def petitions_stats(db: Session = Depends(get_db)):
    rows = db.execute(sqltext("SELECT * FROM petition_stats ORDER BY created_date DESC")).mappings().all()
    return [dict(r) for r in rows]

@router.get("/signatures")
def signatures_stats(db: Session = Depends(get_db)):
    rows = db.execute(sqltext("""
        SELECT petition_id, COUNT(*) AS total
        FROM signatures
        GROUP BY petition_id
        ORDER BY total DESC
    """)).mappings().all()
    return [dict(r) for r in rows]

@router.get("/campaigns")
def campaigns_stats(db: Session = Depends(get_db)):
    rows = db.execute(sqltext("SELECT * FROM campaign_performance ORDER BY created_date DESC")).mappings().all()
    return [dict(r) for r in rows]

@router.get("/growth")
def growth(db: Session = Depends(get_db)):
    rows = db.execute(sqltext("""
        SELECT date_trunc('day', created_date) AS day, COUNT(*) AS total
        FROM signatures
        GROUP BY 1
        ORDER BY 1
    """)).mappings().all()
    return [dict(r) for r in rows]

@router.get("/top-cities")
def top_cities(db: Session = Depends(get_db)):
    rows = db.execute(sqltext("""
        SELECT city, COUNT(*) AS total
        FROM signatures
        WHERE city IS NOT NULL AND city <> ''
        GROUP BY city
        ORDER BY total DESC
        LIMIT 20
    """)).mappings().all()
    return [dict(r) for r in rows]

@router.get("/top-petitions")
def top_petitions(db: Session = Depends(get_db)):
    rows = db.execute(sqltext("""
        SELECT p.id, p.title, COUNT(s.id) AS signatures
        FROM petitions p
        LEFT JOIN signatures s ON s.petition_id = p.id
        GROUP BY p.id, p.title
        ORDER BY signatures DESC
        LIMIT 20
    """)).mappings().all()
    return [dict(r) for r in rows]
