
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
    @classmethod
    def hash_password(cls, password: str) -> str:
        pw_bytes = password.encode("utf-8")
        if len(pw_bytes) > 72:
            pw_bytes = pw_bytes[:72]
        return cls.pwd_context.hash(pw_bytes.decode("utf-8", "ignore"))
    
    
    @classmethod
    def verify_password(cls, password: str, hashed_password: str) -> bool:
        pw_bytes = password.encode("utf-8")
        if len(pw_bytes) > 72:
            pw_bytes = pw_bytes[:72]
        return cls.pwd_context.verify(pw_bytes.decode("utf-8", "ignore"), hashed_password)


    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/login")

    def session_opener(self):
        session = Session(bind=engine)
        try:
            yield session
        finally:
            session.close()

    @classmethod
    def check_user_password_is_correct(cls, db: Session, username: str, password: str):
        user = db.query(User).filter(User.username == username).first()

        if not user:
            raise ValueError("User not found")

        if not cls.verify_password(password, user.hashed_password):
            raise ValueError("Incorrect password")

        return user

    @classmethod
    def authenticate_user_token(
        cls,
        token = Depends(oauth2_scheme),
        db = Depends(session_opener)
    ):
        payload = jwt.decode(token, '1892dhianiandowqd0n', algorithms=["HS256"])
        return db.query(User).filter(User.username == payload.get("sub")).first()

    @classmethod
    def create_access_token(cls,data, expires_delta=None):
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
    

    