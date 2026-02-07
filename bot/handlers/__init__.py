from aiogram import Router
from bot.handlers.user_handlers import router as user_router
from bot.handlers.admin_handlers import admin_router

# Main router that aggregates all other routers
main_router = Router()

# Admin router birinchi bo'lishi kerak (user router state-larni ushlab qolmasligi uchun)
main_router.include_router(admin_router)
main_router.include_router(user_router)
