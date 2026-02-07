import os
from dotenv import load_dotenv

load_dotenv()

print("--- DEBUG INFO ---")
token = os.getenv("BOT_TOKEN")
print(f"Token exists: {bool(token)}")
if token:
    print(f"Token starts with: {token[:10]}...")

raw_ids = os.getenv("ADMIN_IDS")
print(f"Raw ADMIN_IDS in .env: '{raw_ids}'")

try:
    admin_ids = [int(id_str) for id_str in (raw_ids or "").split(",") if id_str.strip()]
    print(f"Parsed ADMIN_IDS list: {admin_ids}")
except Exception as e:
    print(f"Error parsing ADMIN_IDS: {e}")

print("------------------")
