import os
from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from bot.config import TEMP_DIR
from bot.utils.lexicon import USER_TEXTS
from bot.keyboards.user_kb import get_main_keyboard, get_start_keyboard
from bot.services.parser import DocxParser
from bot.services.validator import Validator
from bot.states import ValidatedFileState
from aiogram.types import FSInputFile
from bot.services.processor import Processor
from bot.services.generator import DocxGenerator
from bot.utils.lexicon import BUTTONS

# Module-specific router
user_router = Router()

MAX_FILE_SIZE = 20 * 1024 * 1024  # 20 MB

@user_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        USER_TEXTS["welcome"],
        reply_markup=get_start_keyboard()
    )

from aiogram.filters import Command
@user_router.message(Command(commands=["help"]))
@user_router.message(F.text == BUTTONS["user"]["instructions_btn"])
async def cmd_instructions(message: Message):
    await message.answer(USER_TEXTS["instructions"])

@user_router.message(F.document)
async def handle_document(message: Message, bot: Bot, state: FSMContext):
    document = message.document

    # 1. Extension check
    if not document.file_name.lower().endswith('.docx'):
        await message.answer(USER_TEXTS["wrong_ext"])
        return

    # 2. Size check
    if document.file_size > MAX_FILE_SIZE:
        await message.answer(USER_TEXTS["too_large"])
        return
    
    await message.answer(USER_TEXTS["processing"])

    try:
        # 3. Download file
        file_path = os.path.join(TEMP_DIR, f"{message.from_user.id}_{document.file_name}")
        await bot.download(document, destination=file_path)
        
        # 4. Parse Document
        parser = DocxParser(file_path)
        blocks, errors = parser.parse()
        
        # 5. Validate Blocks
        validator = Validator()
        val_errors = validator.validate(blocks)
        
        all_errors = errors + val_errors
        
        if all_errors:
            # Show top 10 errors
            error_msg = "❌ **Faylda quyidagi xatolar topildi:**\n\n" + "\n".join(all_errors[:10])
            if len(all_errors) > 10:
                error_msg += f"\n\n... va yana {len(all_errors)-10} ta xato."
            await message.answer(error_msg)
            # Cleanup
            try:
                os.remove(file_path)
            except:
                pass
            return

        # 6. Success -> Set State and Show Keyboard
        # We store the file path in state data to use it later
        await state.update_data(file_path=file_path)
        await state.set_state(ValidatedFileState.waiting_for_action)

        await message.answer(
            USER_TEXTS["success"].format(filename=document.file_name),
            reply_markup=get_main_keyboard()
        )




    except Exception as e:
        await message.answer(USER_TEXTS["error"].format(error=str(e)))

@user_router.message(ValidatedFileState.waiting_for_action)
async def handle_action(message: Message, state: FSMContext):
    data = await state.get_data()
    file_path = data.get("file_path")
    
    if not file_path or not os.path.exists(file_path):
        await message.answer("❌ Fayl topilmadi. Iltimos, qaytadan yuboring.")
        await state.clear()
        return

    text = message.text
    valid_buttons = [
        BUTTONS["user"]["shuffle"], 
        BUTTONS["user"]["shuffle_answers"], 
        BUTTONS["user"]["extract"],
        BUTTONS["user"]["back"]
    ]
    
    if text not in valid_buttons:
        await message.answer("Iltimos, tugmalardan birini tanlang.")
        return

    # Handle Restart/Back
    if text == BUTTONS["user"]["back"]:
        await state.clear()
        await message.answer(USER_TEXTS["welcome"], reply_markup=None)
        # Cleanup file if needed
        if file_path and os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass
        return

    await message.answer("⏳ Tayyorlanmoqda...")

    try:
        # 1. Parse again (safe approach to get fresh blocks)
        # Optimization: We could pickle blocks, but parsing is fast enough for <100 pages
        parser = DocxParser(file_path)
        blocks, _ = parser.parse()
        
        # 2. Process
        processor = Processor(blocks)
        processed_blocks = processor.process(text)
        
        # 3. Generate New File
        output_filename = f"gen_{message.from_user.id}_{os.path.basename(file_path)}"
        output_path = os.path.join(TEMP_DIR, output_filename)
        
        generator = DocxGenerator(file_path)
        generator.generate(processed_blocks, output_path)
        
        # 4. Send File
        doc_file = FSInputFile(output_path)
        caption = "✅ Marhamat, tayyor fayl!"
        if text == BUTTONS["user"]["extract"]:
            caption += " (Faqat to'g'ri javoblar)"
        
        await message.answer_document(doc_file, caption=caption)
        
        # 5. Cleanup New File
        # Original file is kept until state is cleared? 
        # Requirement says "Return File & Cleanup". 
        # Maybe we allow multiple actions on same file? 
        # Let's keep state for now so user can click other button too.
        os.remove(output_path)
        
    except Exception as e:
        await message.answer(f"❌ Xatolik: {e}")
