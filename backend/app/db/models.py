from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    salt = Column(String)  # For encryption key derivation
    is_active = Column(Boolean, default=True)

class File(Base):
    __tablename__ = "files"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    filename = Column(String, index=True)
    tags = Column(String)  # JSON string for AI-generated tags
    uploaded_at = Column(DateTime, default=datetime.utcnow)
