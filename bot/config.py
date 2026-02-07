import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = [int(id_str) for id_str in os.getenv("ADMIN_IDS", "").split(",") if id_str.strip()]

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is not set in .env file")

# Temporary directory for file processing
TEMP_DIR = os.path.join(os.getcwd(), "temp_files")
os.makedirs(TEMP_DIR, exist_ok=True)
