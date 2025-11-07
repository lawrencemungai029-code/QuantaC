import logging
import os

LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")
APP_LOG_PATH = os.path.join(LOG_DIR, "app.log")
AI_LOG_PATH = os.path.join(LOG_DIR, "ai.log")

os.makedirs(LOG_DIR, exist_ok=True)

app_logger = logging.getLogger("app")
ai_logger = logging.getLogger("ai")

app_handler = logging.FileHandler(APP_LOG_PATH)
ai_handler = logging.FileHandler(AI_LOG_PATH)

formatter = logging.Formatter(
    "%(asctime)s %(levelname)s %(name)s %(message)s"
)
app_handler.setFormatter(formatter)
ai_handler.setFormatter(formatter)

app_logger.setLevel(logging.INFO)
ai_logger.setLevel(logging.INFO)

if not app_logger.hasHandlers():
    app_logger.addHandler(app_handler)
if not ai_logger.hasHandlers():
    ai_logger.addHandler(ai_handler)
