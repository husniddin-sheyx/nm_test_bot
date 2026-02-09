import os
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from bot.config import TEMP_DIR

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
    from bot.services.database import get_users_count, get_active_users_count
    
    total = get_users_count()
    today = get_active_users_count(days=1)
    week = get_active_users_count(days=7)
    
    text = (
        f"👨‍💻 **Admin Panel (V4.0)**\n\n"
        f"👥 Foydalanuvchilar: **{total}** ta\n"
        f"📅 Bugun faol: **{today}** ta\n"
        f"🗓 Haftalik faol: **{week}** ta\n\n"
        f"Xabar yuborish uchun: /broadcast\n"
        f"Excel yuklash uchun: /export_users"
    )
    await message.answer(text, parse_mode="Markdown")

@admin_router.message(Command("export_users"))
async def cmd_export_users(message: Message, bot: Bot):
    from bot.services.database import get_users_detailed
    import openpyxl
    from openpyxl import Workbook
    from datetime import datetime
    
    await message.answer("⏳ Excel fayl tayyorlanmoqda...")
    
    users = get_users_detailed()
    
    wb = Workbook()
    ws = wb.active
    ws.title = "Foydalanuvchilar"
    
    # Headers
    headers = ["ID", "To'liq ism", "Username", "Qo'shilgan sana", "Oxirgi faollik"]
    ws.append(headers)
    
    # Data
    for user in users:
        ws.append(user)
    
    # Styling (optional but good)
    for cell in ws[1]:
        cell.font = openpyxl.styles.Font(bold=True)
    
    export_filename = f"users_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    export_path = os.path.join(TEMP_DIR, export_filename)
    wb.save(export_path)
    
    try:
        await message.answer_document(
            FSInputFile(export_path), 
            caption=f"✅ Jami foydalanuvchilar: **{len(users)}** ta",
            parse_mode="Markdown"
        )
    except Exception as e:
        await message.answer(f"❌ Faylni yuborishda xatolik: {e}")
    finally:
        if os.path.exists(export_path):
            os.remove(export_path)

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
