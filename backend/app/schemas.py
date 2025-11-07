from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: Optional[str] = "student"
    university: Optional[str] = None
    skills: Optional[str] = None
    portfolio: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class OpportunityBase(BaseModel):
    title: str
    organization: Optional[str] = None
    type: Optional[str] = None
    category: Optional[str] = None
    description: str
    skills: Optional[str] = None
    deadline: Optional[datetime] = None
    posted_date: Optional[datetime] = None
    location: Optional[str] = None
    link: str
    source_url: Optional[str] = None
    is_ai_generated: Optional[bool] = False
    date_scraped: Optional[datetime] = None
    confidence_score: Optional[float] = None
    raw_payload: Optional[str] = None

class OpportunityCreate(OpportunityBase):
    pass

class OpportunityUpdate(OpportunityBase):
    pass

class OpportunityOut(OpportunityBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class ApplicationBase(BaseModel):
    user_id: int
    opportunity_id: int
    status: Optional[str] = "applied"

class ApplicationCreate(ApplicationBase):
    pass

class ApplicationOut(ApplicationBase):
    id: int
    applied_at: datetime

    class Config:
        orm_mode = True

class AiLogOut(BaseModel):
    id: int
    timestamp: datetime
    operation: str
    inserted: int
    updated: int
    duplicates: int
    errors: Optional[str]

    class Config:
        orm_mode = True
