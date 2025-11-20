from ..Loginverification import Loginverification
from ..database import app

from fastapi import APIRouter,Depends

routes=APIRouter()
@app.get("/api/v1/users/me")
def read_users_me(user=Depends(Loginverification.authenticate_user_token)):
    return {"username": user.username}