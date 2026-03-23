from aiogram import Bot
from aiogram.types import BotCommand
from bot.utils.lexicon import COMMANDS_MENU

async def set_main_menu(bot: Bot):
    # Set commands for each language
    for lang, commands in COMMANDS_MENU.items():
        lang_commands = [
            BotCommand(command=cmd, description=desc)
            for cmd, desc in commands.items()
        ]
        # language_code should be one of 'uz', 'ru', 'en'
        await bot.set_my_commands(lang_commands, language_code=lang)
    
    # Also set default commands (Uzbek as default)
    default_commands = [
        BotCommand(command=cmd, description=desc)
        for cmd, desc in COMMANDS_MENU["uz"].items()
    ]
    await bot.set_my_commands(default_commands)
