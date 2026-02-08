from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from bot.filters.admin_filter import AdminFilter
from bot.services.database import get_users_count, get_all_users
from bot.keyboards.user_kb import get_main_keyboard

admin_router = Router()
admin_router.message.filter(AdminFilter())

class BroadcastState(StatesGroup):
    waiting_for_message = State()

@admin_router.message(Command("check"))
async def cmd_check_id(message: Message):
    from bot.config import ADMIN_IDS
    is_admin = message.from_user.id in ADMIN_IDS
    admin_status = "Ha" if is_admin else "Yo'q"
    await message.answer(
        f"🔍 **Diagnostika:**\n"
        f"Sizning ID: `{message.from_user.id}`\n"
        f"Adminlar ro'yxati: `{ADMIN_IDS}`\n"
        f"Adminmisiz?: **{admin_status}**",
        parse_mode="Markdown"
    )

@admin_router.message(Command("admin"))
async def cmd_admin(message: Message):
    count = get_users_count()
    text = (
        f"👨‍💻 **Admin Panel (V3.1)**\n\n"
        f"👥 Foydalanuvchilar soni: **{count}** ta\n\n"
        f"Xabar yuborish uchun: /broadcast"
    )
    await message.answer(text, parse_mode="Markdown")

@admin_router.message(Command("broadcast"))
async def cmd_broadcast(message: Message, state: FSMContext):
    await message.answer("📢 Hammaga yuboriladigan xabarni yozing (matn, rasm, video...):")
    await state.set_state(BroadcastState.waiting_for_message)

@admin_router.message(BroadcastState.waiting_for_message)
async def process_broadcast(message: Message, state: FSMContext, bot: Bot):
    await message.answer("⏳ Xabar yuborish boshlandi...")
    users = get_all_users()
    count = 0
    blocked = 0
    
    for (user_id,) in users:
        try:
            # Copy the message to the user
            await message.send_copy(chat_id=user_id)
            count += 1
        except Exception as e:
            blocked += 1
            
    await message.answer(
        f"✅ Xabar yuborildi!\n\n"
        f"Yuborildi: {count} ta\n"
        f"Bloklaganlar: {blocked} ta"
    )
    await state.clear()
