"""Engine (one per process) and Session (one per request)."""

import os
from urllib.parse import quote_plus

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

DATABASE_URL = (
    f"mysql+pymysql://{os.environ['MYSQL_USER']}:{quote_plus(os.environ['MYSQL_PASSWORD'])}"
    f"@{os.environ['DB_HOST']}:{os.environ['DB_PORT']}/{os.environ['MYSQL_DATABASE']}"
)

# pool_pre_ping checks a pooled connection is still alive before handing it out;
# MySQL drops idle connections after 8 hours.
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(bind=engine, autoflush=False)


def get_db():
    """FastAPI dependency: one Session per request, always closed."""
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
