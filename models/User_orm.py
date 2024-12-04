from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session
from sqlalchemy import Column, Integer, String, ForeignKey

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    nickname = Column(String(255), nullable=False)

    @classmethod
    def get_by_email(cls, db: Session, email: str):
        return db.query(cls).filter(cls.email == email).first()

    @classmethod
    def create(cls, db: Session, email: str, hashed_password: str, nickname: str):
        new_user = cls(email=email, hashed_password=hashed_password, nickname=nickname)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user