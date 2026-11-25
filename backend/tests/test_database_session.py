
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database.session import get_db


def test_database_session_dependency():
    db_generator = get_db()

    db = next(db_generator)

    try:
        assert isinstance(db, Session)

        result = db.execute(text("SELECT 1"))

        assert result.scalar_one() == 1

    finally:
        db_generator.close()
