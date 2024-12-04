from fastapi import HTTPException, Depends
from typing import Optional
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from database.connection import get_db
from database.orm import User
import bcrypt



class UserService:
    encoding: str = "UTF-8"
    secret_key: str = "3a44"
    jwt_algorithm: str = "HS256"


    class UserService:
        secret_key: str = "3a44"
        jwt_algorithm: str = "HS256"
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

        def sign_up(self, db: Session, email: str, password: str, nickname: str) -> bool:
            existing_user = User.get_by_email(db, email)
            if existing_user:
                return False
            hashed_password = self.hash_password(password)
            User.create(db, email=email, hashed_password=hashed_password, nickname=nickname)
            return True

        def authenticate_user(self, db: Session, user_email: str, password: str) -> bool:
            user = User.get_by_email(db, user_email)
            if not user or not self.verify_password(password, user.hashed_password):
                return False
            return True

        def get_nickname(self, db: Session, email: str) -> Optional[str]:
            user = User.get_by_email(db, email)
            if user:
                return user.nickname
            return None

        def change_nickname(self, db: Session, email: str, password: str, new_nickname: str) -> bool:
            user = User.get_by_email(db, email)
            if not user or not self.verify_password(password, user.hashed_password):
                return False
            user.nickname = new_nickname
            db.commit()
            return True

        def change_password(self, db: Session, email: str, current_password: str, new_password: str) -> bool:
            user = User.get_by_email(db, email)
            if not user or not self.verify_password(current_password, user.hashed_password):
                return False
            user.hashed_password = self.hash_password(new_password)
            db.commit()
            return True

        def delete_user(self, db: Session, email: str, password: str) -> bool:
            user = User.get_by_email(db, email)
            if not user or not self.verify_password(password, user.hashed_password):
                return False
            db.delete(user)
            db.commit()
            return True

        def hash_password(self, plain_password: str) -> str:
            return self.pwd_context.hash(plain_password)

        def verify_password(self, plain_password: str, hashed_password: str) -> bool:
            return self.pwd_context.verify(plain_password, hashed_password)

        def create_jwt(self, username: str) -> str:
            to_encode = {
                "sub": username,
                "exp": datetime.now(timezone.utc) + timedelta(days=1)
            }
            return jwt.encode(to_encode, self.secret_key, algorithm=self.jwt_algorithm)

        def decode_jwt(self, token: str) -> dict:
            try:
                payload = jwt.decode(token, self.secret_key, algorithms=[self.jwt_algorithm])
                return payload
            except JWTError:
                raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다.")
