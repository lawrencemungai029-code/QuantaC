import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./opportunities.db")
JWT_SECRET = os.getenv("JWT_SECRET", "supersecretjwtkey")
ASI_ENDPOINT = os.getenv("ASI_ENDPOINT")
ASI_API_KEY = os.getenv("ASI_API_KEY")
INTERNAL_API_KEY = os.getenv("INTERNAL_API_KEY")
SCHEDULE_CRON = os.getenv("SCHEDULE_CRON", "0 */6 * * *")
FUZZY_SIMILARITY_THRESHOLD = float(os.getenv("FUZZY_SIMILARITY_THRESHOLD", 0.85))
EMBEDDING_SIM_THRESHOLD = float(os.getenv("EMBEDDING_SIM_THRESHOLD", 0.85))
CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", 0.60))
ALLOWED_SOURCES = [
    "devpost.com",
    "mlh.io",
    "eventbrite.com",
    "unstop.com",
    "undp.org",
    "unep.org"
]
EXCLUDED_ORIGINS = [
    "linkedin.com"
]
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
ALERT_EMAIL = os.getenv("ALERT_EMAIL")
