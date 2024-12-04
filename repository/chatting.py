from connection import SessionFactory,engine

#  데이터베이스에서 모든 채팅 메시지를 조회
def test_get_all_chat_messages():
    session = SessionFactory()
    try:
        messages = session.query(ChatMessages).all()
        for message in messages:
            print(message)  # __repr__ 메서드에 의해 출력됨
        return messages
    except Exception as e:
        print(f"Error fetching chat messages: {e}")
    finally:
        session.close()
        
# 테스트 코드
if __name__ == "__main__":
    # 테이블 생성 (필요 시)
    Base.metadata.create_all(bind=engine)
    print("Chat messages from database:")
    test_get_all_chat_messages()
