from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.utils.lexicon import LEXICON

def get_admin_main_keyboard(lang: str = "uz") -> InlineKeyboardMarkup:
    """Returns the main admin dashboard keyboard."""
    buttons_text = LEXICON[lang]["buttons"]
    buttons = [
        [
            InlineKeyboardButton(text=buttons_text["stats"], callback_data="admin_stats"),
            InlineKeyboardButton(text=buttons_text["export"], callback_data="admin_export")
        ],
        [
            InlineKeyboardButton(text=buttons_text["broadcast"], callback_data="admin_broadcast")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_admin_back_keyboard(lang: str = "uz") -> InlineKeyboardMarkup:
    """Keyboard with just a back button to admin main menu."""
    buttons_text = LEXICON[lang]["buttons"]
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=buttons_text["back"], callback_data="admin_main")]
    ])

def get_admin_broadcast_confirm_keyboard(lang: str = "uz") -> InlineKeyboardMarkup:
    """Keyboard for broadcast confirmation."""
    buttons_text = LEXICON[lang]["buttons"]
    buttons = [
        [
            InlineKeyboardButton(text=buttons_text["confirm"], callback_data="admin_broadcast_confirm"),
            InlineKeyboardButton(text=buttons_text["cancel"], callback_data="admin_broadcast_cancel")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
