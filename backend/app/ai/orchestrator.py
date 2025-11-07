
import asyncio


from app.logs.logging_config import app_logger, ai_logger
from app.config import ALLOWED_SOURCES, CONFIDENCE_THRESHOLD
from app.ai.asi_integration import extract_opportunities_from_text
from app import crud
from app.ai.fetch_devpost import fetch_devpost, dedupe_opportunities as dedupe_devpost, validate_opportunity as validate_devpost
from app.ai.fetch_mlh import fetch_mlh, dedupe_opportunities as dedupe_mlh, validate_opportunity as validate_mlh
from app.ai.fetch_eventbrite import fetch_eventbrite, dedupe_opportunities as dedupe_eventbrite, validate_opportunity as validate_eventbrite
from app.ai.fetch_unep_undp_kenya import fetch_unep_undp_kenya, dedupe_opportunities as dedupe_undp, validate_opportunity as validate_undp

async def run_orchestrator(db):
    fetchers = [
        (fetch_devpost, dedupe_devpost, validate_devpost),
        (fetch_mlh, dedupe_mlh, validate_mlh),
        (fetch_eventbrite, dedupe_eventbrite, validate_eventbrite),
        (fetch_unep_undp_kenya, dedupe_undp, validate_undp)
    ]
    inserted, updated, duplicates = 0, 0, 0
    all_opps = []
    for fetcher, deduper, validator in fetchers:
        items = await fetcher()
        for item in items:
            raw_text = item['raw_text_or_html']
            extracted = extract_opportunities_from_text(raw_text)
            valid_opps = [opp for opp in extracted if validator(opp, CONFIDENCE_THRESHOLD)]
            deduped_opps = deduper(valid_opps)
            for opp in deduped_opps:
                crud.create_opportunity(db, opp)
                inserted += 1
            all_opps.extend(deduped_opps)
    app_logger.info(f"Orchestrator run: {inserted} inserted, {updated} updated, {duplicates} duplicates")
    crud.log_ai_run(db, "orchestrator_run", inserted, updated, duplicates)
    return {"inserted": inserted, "updated": updated, "duplicates": duplicates}
