
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.ai.asi_integration import extract_opportunities_from_text
from app.deps import get_db, require_role
from app.models import User
from app.logs.logging_config import ai_logger

router = APIRouter()

@router.post("/ai/test", tags=["ai"])
def test_asi_integration(payload: dict, current_user: User = Depends(require_role("admin")), db: Session = Depends(get_db)):
    raw_text = payload.get("raw_text", "Sample opportunity text for ASI1 test.")
    result = extract_opportunities_from_text(raw_text)
    ai_logger.info(f"ASI1 test called by user {current_user.id}")
    return {"result": result}

@router.post("/ai/recommend", tags=["ai"])
def recommend(payload: dict, current_user: User = Depends(require_role("admin")), db: Session = Depends(get_db)):
    # Example: payload = {"query": "machine learning internship"}
    query = payload.get("query", "")
    # Use ASI1 to classify and recommend
    asi_result = extract_opportunities_from_text(query)
    # Ranking logic: sort by confidence_score desc
    ranked = sorted(asi_result, key=lambda x: x.get("confidence_score", 0), reverse=True)
    ai_logger.info(f"ASI1 recommend called by user {current_user.id} for query '{query}'")
    return {"recommendations": ranked}
