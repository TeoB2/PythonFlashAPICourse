from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status, Path
from models import User
from database import SessionLocal
from pydantic import BaseModel, Field
from .auth import get_current_user
from passlib.context import CryptContext


router = APIRouter(
    prefix="/users",
    tags=["users"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db #prima si crea la connessione al db e poi la rilascia
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.get("/users", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')
    
    user_tmp = db.query(User).filter(User.id == user.get('id')).first()

    if user_tmp is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return user_tmp

@router.put("/user/change_password/{user_id}", status_code=status.HTTP_200_OK)
async def change_password(user: user_dependency, db: db_dependency, new_password: str, user_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')
    
    if new_password is None or len(new_password) < 8:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password must be at least 8 characters long")

    user_tmp = db.query(User).filter(User.id == user_id).first()

    if user_tmp is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user_tmp.hashed_password = bcrypt_context.hash(new_password)

    db.add(user_tmp)
    db.commit()

@router.put("/user/change_telephone_number/", status_code=status.HTTP_200_OK)
async def change_telephone_number(user: user_dependency, db: db_dependency, new_telephone_number: str):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')
    
    if new_telephone_number is None or len(new_telephone_number) < 8:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Telephone number must be at least 8 characters long")

    user_tmp = db.query(User).filter(User.id == user.get('id')).first()

    if user_tmp is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user_tmp.phone_number = new_telephone_number

    db.add(user_tmp)
    db.commit()