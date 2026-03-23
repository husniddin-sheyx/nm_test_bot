import os
import shutil
from datetime import datetime
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext

from bot.config import TEMP_DIR, UPLOADS_DIR
from bot.utils.lexicon import LEXICON, ERROR_TEXTS
from bot.services.database import (
    add_user, 
    get_user_language, 
    set_user_language, 
    update_last_active,
    update_user_setting,
    get_user_setting,
    log_file_upload,
    get_user_files_history
)
from bot.keyboards.user_kb import (
    get_language_keyboard, 
    get_main_keyboard, 
    get_settings_keyboard,
    get_action_keyboard
)
from bot.services.parser import DocxParser
from bot.services.validator import Validator
from bot.states import ValidatedFileState
from bot.services.processor import Processor
from bot.services.generator import DocxGenerator

router = Router()

MAX_FILE_SIZE = 10 * 1024 * 1024 # 10MB

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    add_user(message.from_user.id, message.from_user.full_name, message.from_user.username)
    lang = get_user_language(message.from_user.id)
    await message.answer(
        LEXICON[lang]["user"]["welcome"],
        reply_markup=get_main_keyboard(lang=lang)
    )

@router.message(F.text.in_([LEXICON[l]["buttons"]["instructions_btn"] for l in LEXICON]))
async def show_instructions(message: Message, lang: str):
    await message.answer(LEXICON[lang]["user"]["instructions"], parse_mode="Markdown")

@router.message(F.text.in_([LEXICON[l]["buttons"]["settings_btn"] for l in LEXICON]))
async def show_settings(message: Message, lang: str):
    await message.answer(
        LEXICON[lang]["user"]["settings_welcome"],
        reply_markup=get_settings_keyboard(lang=lang)
    )

@router.callback_query(F.data == "set_lang")
async def process_lang_setting(callback: CallbackQuery, lang: str):
    await callback.message.edit_text(
        LEXICON[lang]["user"]["choose_lang"],
        reply_markup=get_language_keyboard()
    )
    await callback.answer()

@router.callback_query(F.data.startswith("lang_"))
async def process_lang_select(callback: CallbackQuery, state: FSMContext):
    new_lang = callback.data.split("_")[1]
    set_user_language(callback.from_user.id, new_lang)
    
    await callback.message.delete()
    await callback.message.answer(
        LEXICON[new_lang]["user"]["settings_updated"],
        reply_markup=get_main_keyboard(lang=new_lang)
    )
    await callback.answer()

@router.callback_query(F.data == "set_mode")
async def process_mode_select(callback: CallbackQuery, lang: str):
    # Toggle or choice logic here
    await callback.answer("Hozircha faqat standart rejim mavjud.")

@router.callback_query(F.data == "settings_back")
async def back_to_settings(callback: CallbackQuery, lang: str):
    await callback.message.edit_text(
        LEXICON[lang]["user"]["settings_welcome"],
        reply_markup=get_settings_keyboard(lang=lang)
    )
    await callback.answer()

@router.message(F.document)
async def handle_document(message: Message, bot: Bot, lang: str, state: FSMContext):
    document = message.document

    # 1. Extension check
    ext = document.file_name.lower().split('.')[-1]
    if ext not in ['docx', 'xlsx']:
        await message.answer(ERROR_TEXTS["no_questions"])
        return

    # 2. Size check
    if document.file_size > MAX_FILE_SIZE:
        await message.answer(LEXICON[lang]["user"]["too_large"])
        return
    
    await message.answer(LEXICON[lang]["user"]["processing"])

    try:
        # Update last active on every file upload
        update_last_active(message.from_user.id)
        
        # 3. Download file
        file_path = os.path.join(TEMP_DIR, f"{message.from_user.id}_{document.file_name}")
        await bot.download(document, destination=file_path)
        
        # 4. Parse Document
        if file_path.endswith('.xlsx'):
            from bot.services.parser import XlsxParser
            parser = XlsxParser(file_path)
        else:
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
            
            # Error report always Docx for now
            generator = DocxGenerator(file_path)
            generator.generate_error_report(invalid_with_errors, report_path)
            
            # Send Report
            await message.answer_document(
                FSInputFile(report_path, filename=report_filename),
                caption=LEXICON[lang]["user"]["error_report_sent"]
            )
            os.remove(report_path)

        if not valid_blocks:
            await message.answer(ERROR_TEXTS["no_questions"])
            if os.path.exists(file_path):
                os.remove(file_path)
            return

        # 7. Prepare 'Clean' Source for Processed Flow
        if invalid_with_errors:
            clean_filename = f"clean_{document.file_name}"
            clean_path = os.path.join(TEMP_DIR, f"{message.from_user.id}_{clean_filename}")
            
            # For now generator only supports docx clean output
            # If input was Xlsx, we might want to convert to Docx here or keep blocks
            # Let's just use the blocks in memory for handle_action
            pass 

        # 8. Save State
        await state.update_data(
            file_path=file_path, 
            original_filename=document.file_name
        )
        await state.set_state(ValidatedFileState.waiting_for_action)

        # 9. Offer Actions
        await message.answer(
            LEXICON[lang]["user"]["success_upload"].format(count=len(valid_blocks)),
            reply_markup=get_action_keyboard(lang=lang)
        )

        # 10. Log to History
        perma_path = os.path.join(UPLOADS_DIR, f"{message.from_user.id}_{int(datetime.now().timestamp())}_{document.file_name}")
        shutil.copy(file_path, perma_path)
        log_file_upload(message.from_user.id, document.file_name, perma_path)

    except Exception as e:
        await message.answer(f"❌ Xatolik: {e}")
        if 'file_path' in locals() and os.path.exists(file_path):
            os.remove(file_path)

@router.message(ValidatedFileState.waiting_for_action, F.text)
async def handle_action(message: Message, state: FSMContext, lang: str):
    data = await state.get_data()
    file_path = data.get("file_path")
    
    if not file_path or not os.path.exists(file_path):
        await message.answer("❌ Fayl topilmadi, iltimos qaytadan yuboring.")
        await state.clear()
        return

    text = message.text
    processor_action = None
    
    # Map text back to action key
    for l in LEXICON:
        if text == LEXICON[l]["buttons"]["shuffle"]:
            processor_action = "shuffle"
            break
        elif text == LEXICON[l]["buttons"]["shuffle_answers"]:
            processor_action = "shuffle_answers"
            break
        elif text == LEXICON[l]["buttons"]["extract"]:
            processor_action = "extract"
            break
    
    if not processor_action:
        return

    await message.answer("⏳ ...")
    update_last_active(message.from_user.id) 

    try:
        # 1. Parse again
        if file_path.endswith('.xlsx'):
            from bot.services.parser import XlsxParser
            parser = XlsxParser(file_path)
        else:
            parser = DocxParser(file_path)
            
        blocks, _ = parser.parse()
        
        # 2. Process
        processor = Processor(blocks)
        processed_blocks = processor.process(processor_action)
        
        # 3. Generate New File
        orig_name = data.get("original_filename", "result.docx")
        name, ext = os.path.splitext(orig_name)
        
        suffix = "_result"
        if file_path.endswith('.xlsx'):
             ext = ".docx" # Always generate Docx for now
            
        new_filename = f"{name}{suffix}{ext}"
        output_path = os.path.join(TEMP_DIR, f"gen_{message.from_user.id}_{new_filename}")
        
        generator = DocxGenerator(file_path)
        generator.generate(processed_blocks, output_path)
        
        # 4. Send File
        doc_file = FSInputFile(output_path, filename=new_filename)
        caption = "✅" 
        if processor_action == "extract":
            caption += " (Pluses)"
        
        await message.answer_document(doc_file, caption=caption)
        
        # 5. Cleanup
        if os.path.exists(output_path):
            os.remove(output_path)
        if os.path.exists(file_path):
            os.remove(file_path)
            
        await state.clear()
            
    except Exception as e:
        if 'file_path' in locals() and os.path.exists(file_path):
            os.remove(file_path)
        await message.answer(f"❌ Xatolik: {e}")

@router.message(F.text.in_([LEXICON[l]["buttons"]["history"] for l in LEXICON]))
async def show_history(message: Message, lang: str):
    files = get_user_files_history(message.from_user.id)
    
    if not files:
        await message.answer(LEXICON[lang]["user"]["no_history"])
        return

    from aiogram.utils.keyboard import InlineKeyboardBuilder
    from aiogram.types import InlineKeyboardButton
    
    builder = InlineKeyboardBuilder()
    for file_id, filename, _, timestamp in files:
        # Show filename and date
        date_str = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S").strftime("%d.%m %H:%M")
        builder.row(InlineKeyboardButton(
            text=f"📄 {filename} ({date_str})", 
            callback_data=f"hist_{file_id}"
        ))
    
    await message.answer(LEXICON[lang]["user"]["history_welcome"], reply_markup=builder.as_markup())

@router.callback_query(F.data.startswith("hist_"))
async def process_history_select(callback: CallbackQuery, state: FSMContext, lang: str):
    file_id = int(callback.data.replace("hist_", ""))
    from bot.services.database import get_file_by_id
    file_data = get_file_by_id(file_id)
    
    if not file_data:
        await callback.answer(LEXICON[lang]["user"]["file_not_found"])
        return
        
    _, filename, storage_path, _ = file_data
    
    if not storage_path or not os.path.exists(storage_path):
        await callback.answer(LEXICON[lang]["user"]["file_not_found"])
        return
        
    # Copy to TEMP for processing
    temp_path = os.path.join(TEMP_DIR, f"{callback.from_user.id}_{filename}")
    shutil.copy(storage_path, temp_path)
    
    await state.update_data(file_path=temp_path, original_filename=filename)
    await state.set_state(ValidatedFileState.waiting_for_action)
    
    await callback.message.answer(
        LEXICON[lang]["user"]["history_reprocess"].format(filename=filename),
        reply_markup=get_action_keyboard(lang=lang)
    )
    await callback.answer()
