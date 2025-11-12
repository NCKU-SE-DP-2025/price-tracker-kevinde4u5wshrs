from ..models import User
from ..database import UserAuthSchema,app
from ..Loginverification import Loginverification

from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session

routes=APIRouter()
@app.post("/api/v1/users/register")
def create_user(user: UserAuthSchema, db: Session = Depends(Loginverification.session_opener)):
    """create user"""
    hashed_password = Loginverification.pwd_context.hash(user.password)
    db_user = User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user