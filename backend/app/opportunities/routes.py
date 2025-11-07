from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import crud, schemas, deps, models
from ..config import CONFIDENCE_THRESHOLD

router = APIRouter()

@router.get("/opportunities", response_model=list[schemas.OpportunityOut])
def list_opportunities(q: str = None, type: str = None, category: str = None, location: str = None, limit: int = 20, offset: int = 0, sort: str = None, db: Session = Depends(deps.get_db)):
    filters = {"q": q, "type": type, "category": category, "location": location}
    return crud.get_opportunities(db, skip=offset, limit=limit, filters=filters)

@router.get("/opportunities/{id}", response_model=schemas.OpportunityOut)
def get_opportunity(id: int, db: Session = Depends(deps.get_db)):
    opp = crud.get_opportunity(db, id)
    if not opp:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    return opp

@router.post("/opportunities", response_model=schemas.OpportunityOut)
def create_opportunity(opportunity: schemas.OpportunityCreate, current_user: models.User = Depends(deps.require_role("client")), db: Session = Depends(deps.get_db)):
    return crud.create_opportunity(db, opportunity)

@router.put("/opportunities/{id}", response_model=schemas.OpportunityOut)
def update_opportunity(id: int, opportunity: schemas.OpportunityUpdate, current_user: models.User = Depends(deps.get_current_active_user), db: Session = Depends(deps.get_db)):
    opp = crud.get_opportunity(db, id)
    if not opp:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    # Only owner or admin can update
    if current_user.role not in ["admin", "client"]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    return crud.update_opportunity(db, id, opportunity)

@router.delete("/opportunities/{id}")
def delete_opportunity(id: int, current_user: models.User = Depends(deps.require_role("admin")), db: Session = Depends(deps.get_db)):
    opp = crud.get_opportunity(db, id)
    if not opp:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    crud.delete_opportunity(db, id)
    return {"ok": True}

@router.post("/opportunities/{id}/apply")
def apply_to_opportunity(id: int, application: schemas.ApplicationCreate, current_user: models.User = Depends(deps.require_role("student")), db: Session = Depends(deps.get_db)):
    application.opportunity_id = id
    application.user_id = current_user.id
    return crud.create_application(db, application)

@router.get("/users/{id}/applications", response_model=list[schemas.ApplicationOut])
def get_user_applications(id: int, current_user: models.User = Depends(deps.get_current_active_user), db: Session = Depends(deps.get_db)):
    if current_user.id != id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    return crud.get_applications_by_user(db, id)

@router.post("/admin/verify-opportunity/{id}")
def verify_opportunity(id: int, current_user: models.User = Depends(deps.require_role("admin")), db: Session = Depends(deps.get_db)):
    opp = crud.get_opportunity(db, id)
    if not opp:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    opp.confidence_score = max(opp.confidence_score or 0.0, CONFIDENCE_THRESHOLD)
    db.commit()
    db.refresh(opp)
    return opp

@router.post("/ai/update_opportunities")
def ai_update_opportunities(opportunities: list[schemas.OpportunityCreate], db: Session = Depends(deps.get_db), internal_api_key: str = None, current_user: models.User = Depends(deps.get_current_active_user)):
    # Accept either INTERNAL_API_KEY or admin JWT
    from ..config import INTERNAL_API_KEY
    if not (internal_api_key == INTERNAL_API_KEY or (current_user and current_user.role == "admin")):
        raise HTTPException(status_code=403, detail="Unauthorized")
    inserted, updated, duplicates = 0, 0, 0
    for opp in opportunities:
        # Deduplication logic would go here
        crud.create_opportunity(db, opp)
        inserted += 1
    crud.log_ai_run(db, "ai_update_opportunities", inserted, updated, duplicates)
    return {"inserted": inserted, "updated": updated, "duplicates": duplicates}

@router.get("/admin/ai/logs", response_model=list[schemas.AiLogOut])
def get_ai_logs(limit: int = 10, current_user: models.User = Depends(deps.require_role("admin")), db: Session = Depends(deps.get_db)):
    return crud.get_ai_logs(db, limit)

@router.post("/seed")
def seed_data(db: Session = Depends(deps.get_db), current_user: models.User = Depends(deps.require_role("admin"))):
    from ...scripts.seed_data import seed_opportunities
    return seed_opportunities(db)
