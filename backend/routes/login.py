from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from model import User
from auth import create_token

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/login")
def login(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()

    if not user or user.password != password:
        return {"error": "Invalid credentials"}

    token = create_token({"username": user.username, "role": user.role})

    return {
        "access_token": token,
        "role": user.role
    }

