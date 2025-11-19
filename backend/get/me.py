from Loginverification import Loginverification
from fastapi import APIRouter,Depends

routes=APIRouter()
@routes.get("/api/v1/users/me")
def read_users_me(user=Depends(Loginverification.authenticate_user_token)):
    return {"username": user.username}

