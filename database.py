from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Corrected database URL format for MySQL: mysql+pymysql://username:password@host/database_name
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:Shema0987!!!@localhost/Pets"  # Corrected the database name to 'Pets'

# Create the engine
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_size=10, max_overflow=20)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()
