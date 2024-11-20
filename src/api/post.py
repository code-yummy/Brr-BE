from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from database.orm import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    body = Column(String, nullable=False)
    user_id = Column(String, ForeignKey("users.id"))

    user = relationship("User", back_populates="posts")

    def __init__(self, title: str, body: str, user_id: str):
        self.title = title
        self.body = body
        self.user_id = user_id
