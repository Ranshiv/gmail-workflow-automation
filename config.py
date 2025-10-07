import os

from dotenv import load_dotenv

load_dotenv()

SCOPES = [
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.compose",
]
CREDENTIALS_FILE = os.path.join("credentials", "credentials.json")
TOKEN_FILE = os.path.join("credentials", "token.json")

JOB_KEYWORDS = [
    "application",
    "job",
    "resume",
    "cover letter",
    "position",
    "career",
    "opportunity",
    "applied",
    "applying",
    "hire",
    "employment",
    "vacancy",
    "role",
    "interview",
]

RESEND_PREFIX = "Resending:"
RESEND_MESSAGE = """Resending this application in case it was missed. Kindly confirm receipt. Thank you!\n\n---Original Message---\n"""

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.path.join("logs", "resender.log")
DRY_RUN = os.getenv("DRY_RUN", "False").lower() == "true"
INTERACTIVE_MODE = os.getenv("INTERACTIVE_MODE", "True").lower() == "true"
EXCLUSION_FILE = os.getenv("EXCLUSION_FILE", "excluded_emails.txt")
AUTO_EXCLUDE_AFTER_SEND = os.getenv("AUTO_EXCLUDE_AFTER_SEND", "True").lower() == "true"
MAX_EMAILS_PER_RECIPIENT = int(os.getenv("MAX_EMAILS_PER_RECIPIENT", "2"))
MAX_EMAILS_PER_RUN = int(os.getenv("MAX_EMAILS_PER_RUN", "200"))
SEND_DELAY = float(os.getenv("SEND_DELAY", "2.0"))
