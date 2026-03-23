import sys
import os
import asyncio
from unittest.mock import MagicMock

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bot.handlers.admin_handlers import generate_user_export
from bot.services.database import init_db, add_user

async def test_export():
    init_db()
    # Add some dummy users with various characters
    add_user(123, "Test User 😊", "testuser")
    add_user(456, "O'tkirbek Qosimov", None)
    
    print("Generating export...")
    try:
        path = await generate_user_export()
        print(f"Export successful: {path}")
        if os.path.exists(path):
            os.remove(path)
    except Exception as e:
        print(f"Export FAILED: {e}")

if __name__ == "__main__":
    asyncio.run(test_export())
