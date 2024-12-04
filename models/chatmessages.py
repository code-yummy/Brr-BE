from sqlalchemy import Boolean, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base,session
from datetime import datetime, timezone
from connection import SessionFactory,engine

Base = declarative_base()

class ChatMessages(Base):
    __tablename__="chat_messages"

    chat_id = Column(Integer,nullable=False,primary_key=True,index=True)
    message = Column(String(10000),nullable=False)
    is_query=Column(Boolean,nullable=False)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"ChatMessages(chat_id={self.chat_id}, messages={self.message}, is_query={self.is_query}, time={self.timestamp})"



# 테스트 코드
if __name__ == "__main__":
    # 테이블 생성 (필요 시)
    Base.metadata.create_all(bind=engine)
    print("Chat messages from database:")
    test_get_all_chat_messages()
