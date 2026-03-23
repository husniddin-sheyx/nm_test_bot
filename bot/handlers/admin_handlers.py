import os
import asyncio
import openpyxl
from openpyxl import Workbook
from datetime import datetime
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.exceptions import TelegramRetryAfter, TelegramForbiddenError, TelegramAPIError

from bot.config import TEMP_DIR
from bot.filters.admin_filter import AdminFilter
from bot.services.database import (
    get_users_count, 
    get_all_users, 
    get_active_users_count,
    get_users_detailed,
    get_total_files_count,
    get_files_count_period
)
from bot.utils.lexicon import ADMIN_TEXTS, BUTTONS
from bot.keyboards.admin_kb import (
    get_admin_main_keyboard, 
    get_admin_back_keyboard,
    get_admin_broadcast_confirm_keyboard
)

admin_router = Router()
admin_router.message.filter(AdminFilter())
admin_router.callback_query.filter(AdminFilter())

class BroadcastState(StatesGroup):
    waiting_for_message = State()

# --- Shared Logic Functions ---

async def get_stats_text() -> str:
    total_users = get_users_count()
    active_today = get_active_users_count(days=1)
    
    total_files = get_total_files_count()
    files_today = get_files_count_period(days=1)
    files_week = get_files_count_period(days=7)
    
    return ADMIN_TEXTS["stats"].format(
        total=total_users, 
        today=active_today, 
        total_files=total_files,
        files_today=files_today,
        files_week=files_week
    )

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
async def process_broadcast_preview(message: Message, state: FSMContext):
    # Store the message ID for copying
    await state.update_data(broadcast_message_id=message.message_id, from_chat_id=message.chat.id)
    
    # Show preview
    await message.send_copy(chat_id=message.chat.id)
    await message.answer(
        ADMIN_TEXTS["broadcast_preview"],
        reply_markup=get_admin_broadcast_confirm_keyboard(),
        parse_mode="Markdown"
    )

@admin_router.callback_query(F.data == "admin_broadcast_confirm")
async def process_broadcast_confirm(callback: CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    msg_id = data.get("broadcast_message_id")
    from_chat = data.get("from_chat_id")
    
    if not msg_id:
        await callback.answer("❌ Xabar topilmadi.")
        return

    users = get_all_users()
    total_users = len(users)
    count = 0
    blocked = 0
    errors = 0
    
    await callback.message.edit_text(f"⏳ Yuborilmoqda: 0/{total_users}...")
    
    for i, (user_id,) in enumerate(users, 1):
        try:
            # Safe copying
            await bot.copy_message(
                chat_id=user_id,
                from_chat_id=from_chat,
                message_id=msg_id
            )
            count += 1
            
            # Anti-flood delay: 20 messages per second (max is 30)
            await asyncio.sleep(0.05)
            
        except TelegramRetryAfter as e:
            # Respect Telegram's request to wait
            await asyncio.sleep(e.retry_after)
            # Try again once after waiting
            try:
                await bot.copy_message(chat_id=user_id, from_chat_id=from_chat, message_id=msg_id)
                count += 1
            except:
                errors += 1
                
        except TelegramForbiddenError:
            # Bot was blocked by user
            blocked += 1
        except TelegramAPIError:
            # Other Telegram errors
            errors += 1
        except Exception:
            errors += 1
            
        # Update status every 50 users to show progress
        if i % 50 == 0:
            try:
                await callback.message.edit_text(f"⏳ Yuborilmoqda: {i}/{total_users}...")
            except:
                pass # Avoid 'message is not modified' error

    await callback.message.answer(
        ADMIN_TEXTS["broadcast_done"].format(count=count, blocked=blocked) + 
        (f"\n❌ Xatoliklar: {errors}" if errors > 0 else ""),
        reply_markup=get_admin_main_keyboard(),
        parse_mode="Markdown"
    )
    await state.clear()
    await callback.answer()

@admin_router.callback_query(F.data == "admin_broadcast_cancel")
async def process_broadcast_cancel(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(
        ADMIN_TEXTS["broadcast_cancelled"],
        reply_markup=get_admin_main_keyboard()
    )
    await callback.answer()
