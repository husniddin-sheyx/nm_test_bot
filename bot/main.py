import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from bot.config import BOT_TOKEN
from bot.handlers import main_router
from bot.keyboards.main_menu import set_main_menu
from bot.services.database import init_db

# Configure logging
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

async def main():
    init_db()
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # Include the main router which holds all sub-routers
    dp.include_router(main_router)
    
    # Set Bot Commands Menu
    from bot.keyboards.main_menu import set_main_menu
    await set_main_menu(bot)

    try:
        logging.info("Bot starting with Modular Architecture...")
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"Error occurred: {e}")
    finally:
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Bot stopped!")
