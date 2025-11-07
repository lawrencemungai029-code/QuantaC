from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, Text, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, default="student")
    university = Column(String, nullable=True)
    skills = Column(String, nullable=True)
    portfolio = Column(String, nullable=True)
    created_at = Column(DateTime, default=func.now())

class Opportunity(Base):
    __tablename__ = "opportunities"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    organization = Column(String, nullable=True)
    type = Column(String, nullable=True)
    category = Column(String, nullable=True)
    description = Column(Text, nullable=False)
    skills = Column(String, nullable=True)
    deadline = Column(DateTime, nullable=True)
    posted_date = Column(DateTime, nullable=True)
    location = Column(String, nullable=True)
    link = Column(String, nullable=False)
    source_url = Column(String, nullable=True, index=True)
    is_ai_generated = Column(Boolean, default=False)
    date_scraped = Column(DateTime, nullable=True)
    confidence_score = Column(Float, nullable=True)
    raw_payload = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class Application(Base):
    __tablename__ = "applications"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    opportunity_id = Column(Integer, ForeignKey('opportunities.id'))
    status = Column(String, default="applied")
    applied_at = Column(DateTime, default=func.now())

class AiLog(Base):
    __tablename__ = "ai_logs"
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=func.now())
    operation = Column(String)
    inserted = Column(Integer)
    updated = Column(Integer)
    duplicates = Column(Integer)
    errors = Column(Text, nullable=True)
