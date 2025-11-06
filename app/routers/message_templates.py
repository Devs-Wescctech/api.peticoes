from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from app.schemas.message_templates import MessageTemplateIn, MessageTemplateOut
from app.models.message_templates import MessageTemplate
from app.core.tenancy import get_session_maker_for_request

router = APIRouter(prefix="/message-templates", tags=["Modelos de Mensagem"])

def get_db(request: Request):
    SessionLocal = get_session_maker_for_request(request)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("", response_model=list[MessageTemplateOut])
def list_templates(type: str | None = None, is_default: bool | None = None, db: Session = Depends(get_db)):
    q = db.query(MessageTemplate)
    if type:
        q = q.filter(MessageTemplate.type == type)
    if is_default is not None:
        q = q.filter(MessageTemplate.is_default == is_default)
    return q.order_by(MessageTemplate.created_date.desc()).all()

@router.post("", response_model=MessageTemplateOut)
def create_template(payload: MessageTemplateIn, db: Session = Depends(get_db)):
    item = MessageTemplate(**payload.dict())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@router.get("/{id}", response_model=MessageTemplateOut)
def get_template(id: str, db: Session = Depends(get_db)):
    item = db.get(MessageTemplate, id)
    if not item:
        raise HTTPException(404, "Template não encontrado")
    return item

@router.put("/{id}", response_model=MessageTemplateOut)
def update_template(id: str, payload: MessageTemplateIn, db: Session = Depends(get_db)):
    item = db.get(MessageTemplate, id)
    if not item:
        raise HTTPException(404, "Template não encontrado")
    for k, v in payload.dict().items():
        setattr(item, k, v)
    db.commit()
    db.refresh(item)
    return item

@router.delete("/{id}")
def delete_template(id: str, db: Session = Depends(get_db)):
    item = db.get(MessageTemplate, id)
    if not item:
        raise HTTPException(404, "Template não encontrado")
    db.delete(item)
    db.commit()
    return {"ok": True}

@router.get("/defaults")
def default_templates(db: Session = Depends(get_db)):
    return db.query(MessageTemplate).filter(MessageTemplate.is_default == True).all()
