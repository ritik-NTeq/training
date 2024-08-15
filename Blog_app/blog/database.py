from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

username = "postgres"
password = "root"
hostname = "localhost"
port = "5432"
dbname="blog"
SQLALCHEMY_DATABASE_URL = f'postgresql://{username}:{password}@{hostname}:{port}/{dbname}'
# SQLALCHEMY_DATABASE_URL = 'sqlite:///./blog.db'

# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})   # connect_args required for sqlite DB only
engine = create_engine(SQLALCHEMY_DATABASE_URL)
# Creating SQL Alchemy engine

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
# Creating a SessionLocal class. Now each instance of sessionLocal will be a Database Session.

Base = declarative_base()
# Creating a base class. Will be inherited for creating models later

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
