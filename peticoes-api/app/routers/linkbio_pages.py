from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from app.schemas.linkbio_pages import LinkBioPageIn, LinkBioPageOut
from app.models.linkbio_pages import LinkBioPage
from app.core.tenancy import get_session_maker_for_request

router = APIRouter(prefix="/linkbio-pages", tags=["Páginas LinkBio"])

def get_db(request: Request):
    SessionLocal = get_session_maker_for_request(request)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("", response_model=list[LinkBioPageOut])
def list_pages(db: Session = Depends(get_db)):
    return db.query(LinkBioPage).order_by(LinkBioPage.created_date.desc()).all()

@router.post("", response_model=LinkBioPageOut)
def create_page(payload: LinkBioPageIn, db: Session = Depends(get_db)):
    item = LinkBioPage(**payload.dict())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@router.get("/{id}", response_model=LinkBioPageOut)
def get_page(id: str, db: Session = Depends(get_db)):
    item = db.get(LinkBioPage, id)
    if not item:
        raise HTTPException(404, "Página não encontrada")
    return item

@router.put("/{id}", response_model=LinkBioPageOut)
def update_page(id: str, payload: LinkBioPageIn, db: Session = Depends(get_db)):
    item = db.get(LinkBioPage, id)
    if not item:
        raise HTTPException(404, "Página não encontrada")
    for k, v in payload.dict().items():
        setattr(item, k, v)
    db.commit()
    db.refresh(item)
    return item

@router.delete("/{id}")
def delete_page(id: str, db: Session = Depends(get_db)):
    item = db.get(LinkBioPage, id)
    if not item:
        raise HTTPException(404, "Página não encontrada")
    db.delete(item)
    db.commit()
    return {"ok": True}

@router.get("/slug/{slug}", response_model=LinkBioPageOut)
def get_page_by_slug(slug: str, db: Session = Depends(get_db)):
    item = db.query(LinkBioPage).filter(LinkBioPage.slug == slug).first()
    if not item:
        raise HTTPException(404, "Página não encontrada")
    return item

@router.get("/{id}/analytics")
def page_analytics(id: str, db: Session = Depends(get_db)):
    item = db.get(LinkBioPage, id)
    if not item:
        raise HTTPException(404, "Página não encontrada")
    return {"views_count": item.views_count, "clicks_count": item.clicks_count}
