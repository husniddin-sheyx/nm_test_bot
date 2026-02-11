from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.utils.lexicon import BUTTONS

def get_admin_main_keyboard() -> InlineKeyboardMarkup:
    """Returns the main admin dashboard keyboard."""
    buttons = [
        [
            InlineKeyboardButton(text=BUTTONS["admin"]["stats"], callback_data="admin_stats"),
            InlineKeyboardButton(text=BUTTONS["admin"]["export"], callback_data="admin_export")
        ],
        [
            InlineKeyboardButton(text=BUTTONS["admin"]["broadcast"], callback_data="admin_broadcast")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_admin_back_keyboard() -> InlineKeyboardMarkup:
    """Keyboard with just a back button to admin main menu."""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=BUTTONS["admin"]["back"], callback_data="admin_main")]
    ])
