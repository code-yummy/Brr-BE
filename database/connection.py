import sys
import os

# 프로젝트 루트를 Python 경로에 추가
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)


from sqlalchemy import create_engine,text
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+pymysql://root:password@127.0.0.1:3306/brr"

engine = create_engine(DATABASE_URL, echo=True)
SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)

##test
def test_database_connection():
    try:
        session = SessionFactory()
        result = session.execute(text("SELECT 1"))
        print("Database connection successful:", result.scalar())
    except Exception as e:
        print("Database connection failed:", str(e))
    finally:
        session.close()

if __name__ == "__main__":
    test_database_connection()