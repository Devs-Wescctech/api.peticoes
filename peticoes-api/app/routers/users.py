from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from app.schemas.users import UserOut
from app.models.users import User
from app.core.tenancy import get_session_maker_for_request

router = APIRouter(prefix="/users", tags=["Usuários"])

def get_db(request: Request):
    SessionLocal = get_session_maker_for_request(request)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db)):
    return db.query(User).limit(200).all()
