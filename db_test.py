from sqlalchemy import text

from app.db.session import SessionLocal


def test_db_connection() -> None:
    db = SessionLocal()
    try:
        db.execute(text("SELECT 1"))
        print("DB connection OK")
    finally:
        db.close()


if __name__ == "__main__":
    test_db_connection()

