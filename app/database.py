from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database connection URL
# Format: '<databasename>://<username>:<password>@<host/remote ip>/<database_name>'
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:R!$H!2003@localhost/fastapi'

# Create the SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define the base class for model
Base = declarative_base()

# Dependency function to provide database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
