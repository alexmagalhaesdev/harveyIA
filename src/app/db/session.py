from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Generator

from core.config import settings


engine = create_engine(settings.database.DATABASE_URL)

SESSIONLOCAL = sessionmaker(autoflush=False, autocommit=False, bind=engine)


def get_db_session() -> Generator:
    try:
        db = SESSIONLOCAL()
        yield db
    finally:
        db.close()
