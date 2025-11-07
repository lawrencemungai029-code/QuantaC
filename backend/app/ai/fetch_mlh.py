
import aiohttp

from datetime import datetime
from app.logs.logging_config import ai_logger

async def fetch_mlh():
    url = "https://mlh.io/seasons/2025/events"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            html = await resp.text()
            ai_logger.info(f"Fetched MLH events at {datetime.utcnow().isoformat()}")
            return [{
                "source": "mlh",
                "url": url,
                "fetched_at": datetime.utcnow().isoformat(),
                "raw_text_or_html": html
            }]

def dedupe_opportunities(opps):
    seen = set()
    deduped = []
    for opp in opps:
        key = (opp.get("title"), opp.get("organization"), opp.get("link"), opp.get("posted_date"))
        if key not in seen:
            seen.add(key)
            deduped.append(opp)
    ai_logger.info(f"Deduped opportunities: {len(deduped)} out of {len(opps)}")
    return deduped

def validate_opportunity(opp, confidence_threshold=0.6):
    required = ["title", "description", "link"]
    valid = all(opp.get(f) for f in required) and (opp.get("confidence_score", 0) >= confidence_threshold)
    if not valid:
        ai_logger.warning(f"Invalid opportunity: {opp.get('title')}")
    return valid
