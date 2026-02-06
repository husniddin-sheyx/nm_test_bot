from aiogram import Router
from bot.handlers.user_handlers import user_router
# from bot.handlers.admin_handlers import admin_router  # Future use

# Main router that aggregates all other routers
main_router = Router()

main_router.include_router(user_router)
# main_router.include_router(admin_router)
