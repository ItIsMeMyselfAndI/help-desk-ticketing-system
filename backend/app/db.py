from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    from app.models import Base
    Base.metadata.create_all(bind=engine)
    print("Database initialized.")

def drop_db():
    from app.models import Base
    Base.metadata.drop_all(bind=engine)
    print("Database dropped.")
