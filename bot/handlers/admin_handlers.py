import os
import openpyxl
from openpyxl import Workbook
from datetime import datetime
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from bot.config import TEMP_DIR
from bot.filters.admin_filter import AdminFilter
from bot.services.database import (
    get_users_count, 
    get_all_users, 
    get_active_users_count,
    get_users_detailed
)
from bot.utils.lexicon import ADMIN_TEXTS, BUTTONS
from bot.keyboards.admin_kb import get_admin_main_keyboard, get_admin_back_keyboard

admin_router = Router()
admin_router.message.filter(AdminFilter())
admin_router.callback_query.filter(AdminFilter())

class BroadcastState(StatesGroup):
    waiting_for_message = State()

# --- Shared Logic Functions ---

async def get_stats_text() -> str:
    total = get_users_count()
    today = get_active_users_count(days=1)
    week = get_active_users_count(days=7)
    return ADMIN_TEXTS["stats"].format(total=total, today=today, week=week)

async def generate_user_export() -> str:
    users = get_users_detailed()
    wb = Workbook()
    ws = wb.active
    ws.title = "Foydalanuvchilar"
    
    headers = ["ID", "To'liq ism", "Username", "Qo'shilgan sana", "Oxirgi faollik"]
    ws.append(headers)
    for user in users:
        ws.append(user)
        
    for cell in ws[1]:
        cell.font = openpyxl.styles.Font(bold=True)
    
    filename = f"users_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    path = os.path.join(TEMP_DIR, filename)
    wb.save(path)
    return path

# --- Message Handlers ---

@admin_router.message(Command("admin"))
async def cmd_admin(message: Message):
    await message.answer(
        ADMIN_TEXTS["welcome"],
        reply_markup=get_admin_main_keyboard(),
        parse_mode="Markdown"
    )

@admin_router.message(Command("check"))
async def cmd_check_id(message: Message):
    from bot.config import ADMIN_IDS
    is_admin = message.from_user.id in ADMIN_IDS
    await message.answer(
        f"🔍 **Diagnostika:**\nSizning ID: `{message.from_user.id}`\nAdminmisiz?: **{'Ha' if is_admin else 'Yo''q'}**",
        parse_mode="Markdown"
    )

# --- Callback Handlers ---

@admin_router.callback_query(F.data == "admin_main")
async def back_to_main(callback: CallbackQuery):
    await callback.message.edit_text(
        ADMIN_TEXTS["welcome"],
        reply_markup=get_admin_main_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()

@admin_router.callback_query(F.data == "admin_stats")
async def show_stats(callback: CallbackQuery):
    text = await get_stats_text()
    await callback.message.edit_text(
        text,
        reply_markup=get_admin_back_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()

@admin_router.callback_query(F.data == "admin_export")
async def export_users_callback(callback: CallbackQuery):
    await callback.answer("⏳ Tayyorlanmoqda...")
    path = await generate_user_export()
    
    try:
        await callback.message.answer_document(
            FSInputFile(path),
            caption=f"✅ Jami foydalanuvchilar ro'yxati."
        )
    except Exception as e:
        await callback.message.answer(f"❌ Xatolik: {e}")
    finally:
        if os.path.exists(path):
            os.remove(path)

@admin_router.callback_query(F.data == "admin_broadcast")
async def broadcast_start_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        ADMIN_TEXTS["broadcast_start"],
        reply_markup=get_admin_back_keyboard(),
        parse_mode="Markdown"
    )
    await state.set_state(BroadcastState.waiting_for_message)
    await callback.answer()

# --- Broadcast Flow ---

@admin_router.message(BroadcastState.waiting_for_message)
async def process_broadcast(message: Message, state: FSMContext, bot: Bot):
    if message.text == BUTTONS["admin"]["back"]: # This might not work if they use text, but we have the button
        await state.clear()
        return

    msg = await message.answer(ADMIN_TEXTS["broadcast_confirm"])
    users = get_all_users()
    count = 0
    blocked = 0
    
    for (user_id,) in users:
        try:
            await message.send_copy(chat_id=user_id)
            count += 1
        except:
            blocked += 1
            
    await msg.edit_text(
        ADMIN_TEXTS["broadcast_done"].format(count=count, blocked=blocked),
        reply_markup=get_admin_main_keyboard()
    )
    await state.clear()
