from sqlalchemy.orm import Session
from . import models, schemas
from typing import List, Optional
from sqlalchemy import or_

# User CRUD

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate, password_hash: str):
    db_user = models.User(
        name=user.name,
        email=user.email,
        password_hash=password_hash,
        role=user.role,
        university=user.university,
        skills=user.skills,
        portfolio=user.portfolio
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Opportunity CRUD

def get_opportunities(db: Session, skip: int = 0, limit: int = 20, filters: Optional[dict] = None):
    query = db.query(models.Opportunity)
    if filters:
        if "q" in filters:
            query = query.filter(or_(models.Opportunity.title.ilike(f"%{filters['q']}%"), models.Opportunity.description.ilike(f"%{filters['q']}%")))
        if "type" in filters:
            query = query.filter(models.Opportunity.type == filters["type"])
        if "category" in filters:
            query = query.filter(models.Opportunity.category == filters["category"])
        if "location" in filters:
            query = query.filter(models.Opportunity.location == filters["location"])
        if "verified" in filters:
            query = query.filter(models.Opportunity.confidence_score >= 0.6)
        if "ai_sourced" in filters:
            query = query.filter(models.Opportunity.is_ai_generated == True)
        if "deadline_before" in filters:
            query = query.filter(models.Opportunity.deadline <= filters["deadline_before"])
    return query.offset(skip).limit(limit).all()

def get_opportunity(db: Session, opportunity_id: int):
    return db.query(models.Opportunity).filter(models.Opportunity.id == opportunity_id).first()

def create_opportunity(db: Session, opportunity: schemas.OpportunityCreate):
    db_opp = models.Opportunity(**opportunity.dict())
    db.add(db_opp)
    db.commit()
    db.refresh(db_opp)
    return db_opp

def update_opportunity(db: Session, opportunity_id: int, opportunity: schemas.OpportunityUpdate):
    db_opp = get_opportunity(db, opportunity_id)
    if not db_opp:
        return None
    for key, value in opportunity.dict(exclude_unset=True).items():
        setattr(db_opp, key, value)
    db.commit()
    db.refresh(db_opp)
    return db_opp

def delete_opportunity(db: Session, opportunity_id: int):
    db_opp = get_opportunity(db, opportunity_id)
    if db_opp:
        db.delete(db_opp)
        db.commit()
    return db_opp

# Application CRUD

def create_application(db: Session, application: schemas.ApplicationCreate):
    db_app = models.Application(**application.dict())
    db.add(db_app)
    db.commit()
    db.refresh(db_app)
    return db_app

def get_applications_by_user(db: Session, user_id: int):
    return db.query(models.Application).filter(models.Application.user_id == user_id).all()

# AI Log CRUD

def log_ai_run(db: Session, operation: str, inserted: int, updated: int, duplicates: int, errors: Optional[str] = None):
    db_log = models.AiLog(
        operation=operation,
        inserted=inserted,
        updated=updated,
        duplicates=duplicates,
        errors=errors
    )
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

def get_ai_logs(db: Session, limit: int = 10):
    return db.query(models.AiLog).order_by(models.AiLog.timestamp.desc()).limit(limit).all()
