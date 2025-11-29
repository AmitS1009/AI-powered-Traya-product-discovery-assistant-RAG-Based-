from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Default to local postgres if not set
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://neondb_owner:npg_2dJrW3HaDhwo@ep-late-darkness-adbnwn98-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
