from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase

from app.config import settings


engine = create_engine(
    settings.DATABASE_URL,
    echo=False,
    future=True,
)


class Base(DeclarativeBase):
    pass