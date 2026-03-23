from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from bot.utils.lexicon import LEXICON

def get_main_keyboard(lang: str = "uz") -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    buttons = LEXICON[lang]["buttons"]
    
    builder.row(
        KeyboardButton(text=buttons["shuffle"]),
        KeyboardButton(text=buttons["shuffle_answers"])
    )
    builder.row(
        KeyboardButton(text=buttons["extract"]),
        KeyboardButton(text=buttons["back"])
    )
    
    return builder.as_markup(resize_keyboard=True)

def get_start_keyboard(lang: str = "uz", is_admin: bool = False):
    builder = ReplyKeyboardBuilder()
    buttons = LEXICON[lang]["buttons"]
    
    builder.row(
        KeyboardButton(text=buttons["instructions_btn"]),
        KeyboardButton(text=buttons["history"]),
        KeyboardButton(text=buttons["settings_btn"])
    )
    if is_admin:
        builder.row(KeyboardButton(text=buttons["admin_panel"]))
    return builder.as_markup(resize_keyboard=True)

def get_settings_keyboard(lang: str = "uz"):
    builder = InlineKeyboardBuilder()
    buttons = LEXICON[lang]["buttons"]
    
    builder.row(InlineKeyboardButton(text=buttons["lang"], callback_data="change_lang"))
    
    return builder.as_markup()

def get_lang_selection_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🇺🇿 O'zbek", callback_data="set_lang_uz"),
        InlineKeyboardButton(text="🇷🇺 Русский", callback_data="set_lang_ru"),
        InlineKeyboardButton(text="🇺🇸 English", callback_data="set_lang_en")
    )
    return builder.as_markup()
