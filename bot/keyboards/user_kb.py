from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from bot.utils.lexicon import BUTTONS

def get_main_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    
    builder.row(
        KeyboardButton(text=BUTTONS["user"]["shuffle"]),
        KeyboardButton(text=BUTTONS["user"]["extract"])
    )
    
    return builder.as_markup(resize_keyboard=True)
