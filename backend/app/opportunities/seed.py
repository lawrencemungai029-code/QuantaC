from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, deps, models
from app.schemas import OpportunityCreate
from app.config import CONFIDENCE_THRESHOLD

router = APIRouter()

@router.post("/seed", tags=["admin"])
def seed_db(current_user: models.User = Depends(deps.require_role("admin")), db: Session = Depends(deps.get_db)):
    # Example seed data
    sample_opps = [
        OpportunityCreate(
            title="Seeded Hackathon",
            organization="QuantaCrescent",
            type="Hackathon",
            category="Tech",
            description="Seeded hackathon for admin endpoint.",
            skills="python,fastapi,react",
            deadline=None,
            posted_date=None,
            location="Remote",
            link="https://example.com/seeded-hackathon",
            source_url="https://example.com/seeded-hackathon",
            is_ai_generated=False,
            date_scraped=None,
            confidence_score=1.0,
            raw_payload="Seeded payload"
        ),
    ]
    for opp in sample_opps:
        crud.create_opportunity(db, opp)
    return {"status": "seeded", "count": len(sample_opps)}
