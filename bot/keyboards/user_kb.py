from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from bot.utils.lexicon import BUTTONS

def get_main_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    
    builder.row(
        KeyboardButton(text=BUTTONS["user"]["shuffle"]),
        KeyboardButton(text=BUTTONS["user"]["shuffle_answers"])
    )
    builder.row(
        KeyboardButton(text=BUTTONS["user"]["extract"]),
        KeyboardButton(text=BUTTONS["user"]["back"])
    )
    
    return builder.as_markup(resize_keyboard=True)

def get_start_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text=BUTTONS["user"]["instructions_btn"]),
        KeyboardButton(text=BUTTONS["user"]["settings_btn"])
    )
    return builder.as_markup(resize_keyboard=True)

def get_settings_keyboard(current_mode: str):
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    from aiogram.utils.keyboard import InlineKeyboardBuilder
    
    builder = InlineKeyboardBuilder()
    
    # Modes
    full_text = "✅ To'liq aralashtirish" if current_mode == "shuffle" else "To'liq aralashtirish"
    ans_text = "✅ Faqat javoblar" if current_mode == "shuffle_answers" else "Faqat javoblar"
    
    builder.row(InlineKeyboardButton(text=full_text, callback_data="set_mode_shuffle"))
    builder.row(InlineKeyboardButton(text=ans_text, callback_data="set_mode_shuffle_answers"))
    
    # Language (Future proof)
    # builder.row(InlineKeyboardButton(text="Tilni o'zgartirish 🇺🇿", callback_data="set_lang"))
    
    return builder.as_markup()
