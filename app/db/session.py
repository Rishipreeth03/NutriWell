from collections.abc import Generator

from sqlalchemy.orm import Session

from app.db.database import engine


def get_db() -> Generator[Session, None, None]:
    db = Session(engine)

    try:
        yield db
    finally:
        db.close()