import os
from aiogram import Router, F, Bot
from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext

from bot.config import TEMP_DIR
from bot.utils.lexicon import USER_TEXTS, BUTTONS, ERROR_TEXTS
from bot.services.database import add_user, update_last_active, get_user_setting, update_user_setting
from bot.keyboards.user_kb import get_main_keyboard, get_start_keyboard, get_settings_keyboard
from bot.services.parser import DocxParser
from bot.services.validator import Validator
from bot.states import ValidatedFileState
from bot.services.processor import Processor
from bot.services.generator import DocxGenerator
from bot.services.database import add_user, update_last_active

# Module-specific router
router = Router()

MAX_FILE_SIZE = 20 * 1024 * 1024  # 20 MB

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    # Foydalanuvchini bazaga qo'shish
    add_user(message.from_user.id, message.from_user.full_name, message.from_user.username)
    
    await message.answer(
        USER_TEXTS["welcome"] + "\n\n*(Sizning ID raqamingiz: `" + str(message.from_user.id) + "`)*",
        reply_markup=get_start_keyboard(),
        parse_mode="Markdown"
    )

@router.message(Command("help"))
@router.message(F.text == BUTTONS["user"]["instructions_btn"])
async def cmd_instructions(message: Message):
    await message.answer(USER_TEXTS["instructions"])

@router.message(F.text == BUTTONS["user"]["settings_btn"])
async def handle_settings(message: Message):
    mode = get_user_setting(message.from_user.id, "default_shuffle", "shuffle")
    await message.answer(
        "⚙️ **Sozlamalar**\n\n"
        "Bu yerda siz botning ishlash usulini o'zingizga moslab olishingiz mumkin.\n"
        f"Hozirgi standart usul: **{mode}**",
        reply_markup=get_settings_keyboard(mode),
        parse_mode="Markdown"
    )

@router.callback_query(F.data.startswith("set_mode_"))
async def process_settings_update(callback: CallbackQuery):
    new_mode = callback.data.replace("set_mode_", "")
    update_user_setting(callback.from_user.id, "default_shuffle", new_mode)
    
    await callback.answer(f"✅ Standart usul {new_mode} ga o'zgartirildi.")
    # Refresh keyboard
    await callback.message.edit_reply_markup(reply_markup=get_settings_keyboard(new_mode))

@router.message(F.document)
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
        # Update last active on every file upload
        update_last_active(message.from_user.id)
        
        # 3. Download file
        file_path = os.path.join(TEMP_DIR, f"{message.from_user.id}_{document.file_name}")
        await bot.download(document, destination=file_path)
        
        # 4. Parse Document
        parser = DocxParser(file_path)
        blocks, parse_errors = parser.parse()
        
        # 5. Validate Blocks
        validator = Validator()
        valid_blocks, invalid_with_errors = validator.validate(blocks)
        
        # 6. Handle Categorization Results
        if invalid_with_errors:
            # Generate Error Report
            name, ext = os.path.splitext(document.file_name)
            report_filename = f"{name}_xatolar{ext}"
            report_path = os.path.join(TEMP_DIR, f"report_{message.from_user.id}_{report_filename}")
            
            generator = DocxGenerator(file_path)
            generator.generate_error_report(invalid_with_errors, report_path)
            
            # Send Report
            await message.answer_document(
                FSInputFile(report_path, filename=report_filename),
                caption=USER_TEXTS["error_report_sent"]
            )
            os.remove(report_path)
            
            # --- Admin Alert for Errors ---
            from bot.config import ADMIN_IDS
            error_summary = "\n".join([f"Q{q.id}: {', '.join(errs)}" for q, errs in invalid_with_errors[:5]])
            admin_alert = (
                f"🚨 **Xatoli fayl yuborildi!**\n\n"
                f"Foydalanuvchi: {message.from_user.full_name} (@{message.from_user.username})\n"
                f"Xatolar: {len(invalid_with_errors)} ta\n\n"
                f"Foydalanuvchiga hisobot yuborildi."
            )
            for admin_id in ADMIN_IDS:
                try:
                    await bot.send_message(admin_id, admin_alert)
                except: pass

        if not valid_blocks:
            await message.answer(ERROR_TEXTS["no_questions"])
            if os.path.exists(file_path):
                os.remove(file_path)
            return

        # 7. Prepare 'Clean' Source for Processed Flow
        if invalid_with_errors:
            # We must create a temporary file with ONLY valid blocks 
            # so the Processor doesn't re-encounter invalid ones.
            clean_path = os.path.join(TEMP_DIR, f"clean_{message.from_user.id}_{document.file_name}")
            generator = DocxGenerator(file_path)
            generator.generate(valid_blocks, clean_path)
            
            # Replace file_path with clean one
            os.remove(file_path)
            file_path = clean_path
            
            await message.answer(
                USER_TEXTS["split_results"].format(valid=len(valid_blocks), invalid=len(invalid_with_errors)),
                parse_mode="Markdown"
            )

        # 8. Success -> Set State and Show Keyboard
        await state.update_data(file_path=file_path, original_filename=document.file_name)
        await state.set_state(ValidatedFileState.waiting_for_action)

        await message.answer(
            USER_TEXTS["success"].format(filename=document.file_name),
            reply_markup=get_main_keyboard(),
            parse_mode="Markdown"
        )

    except Exception as e:
        await message.answer(USER_TEXTS["error"].format(error=str(e)))

@router.message(ValidatedFileState.waiting_for_action)
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
        await message.answer(USER_TEXTS["welcome"], reply_markup=get_start_keyboard())
        # Cleanup file if needed
        if file_path and os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass
        return

    await message.answer("⏳ Tayyorlanmoqda...")
    update_last_active(message.from_user.id) # Track active button press

    try:
        # 1. Parse again
        parser = DocxParser(file_path)
        blocks, _ = parser.parse()
        
        # 2. Process
        processor = Processor(blocks)
        processed_blocks = processor.process(text)
        
        # 3. Generate New File
        orig_name = data.get("original_filename", "result.docx")
        name, ext = os.path.splitext(orig_name)
        
        suffix = "_aralashtirilgan"
        if text == BUTTONS["user"]["shuffle_answers"]:
            suffix = "_javoblar_aralash"
        elif text == BUTTONS["user"]["extract"]:
            suffix = "_pluslar"
            
        new_filename = f"{name}{suffix}{ext}"
        output_path = os.path.join(TEMP_DIR, f"gen_{message.from_user.id}_{new_filename}")
        
        generator = DocxGenerator(file_path)
        generator.generate(processed_blocks, output_path)
        
        # 4. Send File
        doc_file = FSInputFile(output_path, filename=new_filename)
        caption = "✅ Marhamat, tayyor fayl!"
        if text == BUTTONS["user"]["extract"]:
            caption += " (Faqat to'g'ri javoblar)"
        
        await message.answer_document(doc_file, caption=caption)
        
        # 5. Cleanup New File
        os.remove(output_path)
        
    except Exception as e:
        await message.answer(f"❌ Xatolik: {e}")
