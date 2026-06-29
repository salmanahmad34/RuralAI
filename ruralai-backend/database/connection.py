from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config.settings import settings

# For SQLite, we disable same thread check. For Postgres, we don't need it.
connect_args = {"check_same_thread": False} if "sqlite" in settings.database_url else {}

# TODO(security): Ensure DB connection utilizes TLS/mTLS when deploying to staging/production.
engine = create_engine(settings.database_url, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """Dependency injection helper for database sessions."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Create all database tables on startup if they do not exist."""
    import database.models
    Base.metadata.create_all(bind=engine)
