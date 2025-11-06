from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from app.core.security import create_access_token, verify_password, get_password_hash
from app.schemas.users import UserCreate, TokenOut, UserOut
from app.models.users import User
from app.core.tenancy import get_session_maker_for_request

router = APIRouter(prefix="/auth", tags=["Auth"])

def get_db(request: Request):
    SessionLocal = get_session_maker_for_request(request)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=UserOut)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    exists = db.query(User).filter(User.email == payload.email).first()
    if exists:
        raise HTTPException(400, "Email já cadastrado")
    user = User(email=payload.email, password=get_password_hash(payload.password),
                full_name=payload.full_name, role=payload.role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/token", response_model=TokenOut)
def login(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password):
        raise HTTPException(401, "Credenciais inválidas")
    token = create_access_token(str(user.id))
    return {"access_token": token, "token_type": "bearer"}
