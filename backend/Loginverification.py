
from sqlalchemy.orm import Session
from fastapi import Depends
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext
from openai import OpenAI
from database import engine
from models import User
class Loginverification:

    def __init__(self, db_session: Session, ai_api_key: str):
        """
        db_session: SQLAlchemy Session
        ai_api_key: OpenAI API Key
        """
        self.db = db_session
        self.ai_key = ai_api_key
        self.ai_client = OpenAI(api_key=self.ai_key)

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/login")


    def session_opener(self):
        session = Session(bind=engine)
        try:
            yield session
        finally:
            session.close()


    def verify(self,p1, p2):
        return self.pwd_context.verify(p1, p2)


    def check_user_password_is_correct(self,db, name, pwd):
        user = db.query(User).filter(User.username == name).first()
        if not self.verify(pwd, user.hashed_password):
            return False
        return user


    def authenticate_user_token(
        self,
        token = Depends(oauth2_scheme),
        db = Depends(session_opener)
    ):
        payload = jwt.decode(token, '1892dhianiandowqd0n', algorithms=["HS256"])
        return db.query(User).filter(User.username == payload.get("sub")).first()


    def create_access_token(self,data, expires_delta=None):
        """create access token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        print(to_encode)
        encoded_jwt = jwt.encode(to_encode, '1892dhianiandowqd0n', algorithm="HS256")
        return encoded_jwt