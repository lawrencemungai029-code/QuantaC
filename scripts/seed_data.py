import sys
import logging
from app.database import SessionLocal
from app.crud import create_opportunity
from app.schemas import OpportunityCreate

logging.basicConfig(filename='logs/app.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger("seed_data")

def seed_opportunities():
    db = SessionLocal()
    sample_opps = [
        OpportunityCreate(
            title="Sample Hackathon",
            organization="QuantaCrescent",
            type="Hackathon",
            category="Tech",
            description="A sample hackathon for seeding.",
            skills="python,fastapi,react",
            deadline=None,
            posted_date=None,
            location="Remote",
            link="https://example.com/hackathon",
            source_url="https://example.com/hackathon",
            is_ai_generated=False,
            date_scraped=None,
            confidence_score=1.0,
            raw_payload="Sample payload"
        ),
        # Add more sample opportunities as needed
    ]
    for opp in sample_opps:
        create_opportunity(db, opp)
        logger.info(f"Seeded opportunity: {opp.title}")
    db.close()

if __name__ == "__main__":
    seed_opportunities()
    print("Seeding complete.")
