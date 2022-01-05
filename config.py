import os

from dotenv import load_dotenv

load_dotenv()

# === EMAIL NOTIFICATION ===

EMAIL_TO = [addr.strip() for addr in os.environ["EMAIL_TO"].split(",")]

EMAIL_FROM = os.environ["EMAIL_FROM"]
EMAIL_FROM_PASS = os.environ["EMAIL_FROM_PASS"]

# === LOGGING ===

LOG_TO_CONSOLE = os.environ.get("LOG_TO_CONSOLE", "true").lower() == "true"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "incremental": False,
    "loggers": {"": {"level": "INFO", "propagate": False}},
}
