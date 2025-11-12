from ..models import User
from ..Loginverification import Loginverification
from ..database import app

from sqlalchemy.orm import Session
from fastapi import APIRouter,Depends
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm

routes=APIRouter()
@app.post("/api/v1/users/login")
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(), 
        db: Session = Depends(Loginverification.session_opener)
):
    """login"""
    u = Loginverification.check_user_password_is_correct(db, form_data.username, form_data.password)
    access_token = Loginverification.create_access_token(
        data={"sub": str(u.username)}, 
        expires_delta=timedelta(minutes=30)
    )
    return {"access_token": access_token, "token_type": "bearer"}