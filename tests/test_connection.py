import pytest
from sqlalchemy import text
from database.connection import SessionFactory

def test_database_connection():
    session = SessionFactory()
    try:
        result = session.execute(text("SELECT 1"))
        assert result.scalar() == 1
        print("Database connection successful!")
    finally:
        session.close()
