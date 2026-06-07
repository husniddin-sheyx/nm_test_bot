# Multilingual Lexicon
LEXICON = {
    "uz": {
        "user": {
            "welcome": "👋 **Salom! Men Test Aralashtiruvchi Botman.**\n\n"
                       "Menga testlaringiz yozilgan **.docx (Word)** yoki **.xlsx (Excel)** faylini yuboring.\n\n"
                       "📌 **Talablar:**\n"
                       "- Fayl formati: **.docx** yoki **.xlsx**\n"
                       "- Har bir savol alohida blok bo'lishi kerak\n"
                       "- Javoblar `+` yoki `=` (to'g'ri) va `-` (noto'g'ri) bilan boshlanishi kerak",
            "wrong_ext": "❌ Iltimos, faqat **.docx** yoki **.xlsx** formatidagi faylni yuboring.",
            "too_large": "❌ Fayl hajmi juda katta (maksimal 10MB).",
            "processing": "⏳ Fayl qabul qilindi. Tekshirilmoqda...",
            "success": "✅ **Fayl muvaffaqiyatli saqlandi!**\n"
                       "📁 Fayl nomi: `{filename}`",
            "success_upload": "✅ **Fayl muvaffaqiyatli yuklandi va tahlil qilindi!**\n"
                              "📊 Jami savollar soni: **{count}** ta.\n\n"
                              "Quyidagi amallardan birini tanlang:",
            "error": "❌ Faylni yuklashda xatolik yuz berdi: {error}",
            "instructions": "📖 **Qo'llanma:** Savol `?` bilan, to'g'ri javoblar `+` yoki `=` bilan, noto'g'ri javoblar `-` bilan boshlanishi kerak.",
            "split_results": "⚠️ **Xatolar topildi!**\n\nMuvaffaqiyatli: **{valid}**\nXatoli: **{invalid}**",
            "error_report_sent": "📁 Xatolar hisoboti yuborildi.",
            "history_welcome": "📂 **Oxirgi yuklangan fayllaringiz:**",
            "history_reprocess": "📄 **{filename}** fayli tanlandi.\n\nQuyidagi amallardan birini tanlang:",
            "no_history": "📭 Sizda yuklangan fayllar yo'q.",
            "file_not_found": "❌ Fayl topilmadi yoki serverdan o'chirib yuborilgan!",
            "lang_select": "🌐 **Tilni tanlang / Выберите язык / Select language**",
            "lang_updated": "✅ Til muvaffaqiyatli o'zgartirildi!",
            "settings_welcome": "⚙️ **Sozlamalar bo'limi**\n\nQuyidagi tugma orqali bot tilini o'zgartirishingiz mumkin:",
            "choose_lang": "🌐 **Tilni tanlang:**",
            "settings_updated": "✅ Sozlamalar yangilandi!"
        },
        "admin": {
            "welcome": "👨‍💻 **Admin Panel**",
            "stats": "📊 **Statistika**\n\n👥 Foydalanuvchilar: {total}\n📅 Bugun faol: {today}\n📁 Fayllar: {total_files}",
            "broadcast_start": "📢 Xabar matnini yuboring:",
            "broadcast_preview": "👆 Xabar ko'rinishi yuqorida. Tasdiqlaysizmi?",
            "broadcast_confirm": "✅ Yuborish boshlandi...",
            "broadcast_done": "✅ Yuborildi: {count}\n🚫 Bloklangan: {blocked}\n⚠️ Xatolar: {errors}",
            "broadcast_cancelled": "❌ Bekor qilindi."
        },
        "buttons": {
            "shuffle": "🔀 To'liq Aralashtirish",
            "shuffle_answers": "🔀 Faqat javoblar",
            "extract": "➕ Pluslarni olish",
            "back": "🔙 Orqaga",
            "instructions_btn": "📚 Qo'llanma",
            "settings_btn": "⚙️ Sozlamalar",
            "history": "📂 Mening fayllarim",
            "admin_panel": "👨‍💻 Admin Panel",
            "lang": "🌐 Tilni o'zgartirish",
            "stats": "📊 Statistika",
            "export": "📥 Export (Excel)",
            "broadcast": "📢 Xabar yuborish",
            "confirm": "✅ Tasdiqlash",
            "cancel": "❌ Bekor qilish"
        }
    },
    "ru": {
        "user": {
            "welcome": "👋 **Привет! Я бот для перемешивания тестов.**\n\n"
                       "Пришлите мне файл **.docx (Word)** или **.xlsx (Excel)** с вашими тестами.\n\n"
                       "📌 **Требования:**\n"
                       "- Формат файла: **.docx** или **.xlsx**\n"
                       "- Каждый вопрос должен быть отдельным блоком\n"
                       "- Ответы должны начинаться с `+` или `=` (верно) и `-` (неверно)",
            "wrong_ext": "❌ Пожалуйста, отправьте файл в формате **.docx** или **.xlsx**.",
            "too_large": "❌ Файл слишком большой (максимум 10МБ).",
            "processing": "⏳ Файл получен. Проверяю...",
            "success": "✅ **Файл успешно сохранен!**\n"
                       "📁 Имя файла: `{filename}`",
            "success_upload": "✅ **Файл успешно загружен и проанализирован!**\n"
                              "📊 Всего вопросов: **{count}**.\n\n"
                              "Выберите одно из действий:",
            "error": "❌ Ошибка при загрузке: {error}",
            "instructions": "📖 **Инструкция:** Вопрос начинается с `?`, правильный ответ с `+` или `=`, неправильный с `-`.",
            "split_results": "⚠️ **Найдены ошибки!**\n\nУспешно: **{valid}**\nС ошибками: **{invalid}**",
            "error_report_sent": "📁 Отчет об ошибках отправлен.",
            "history_welcome": "📂 **Ваши последние файлы:**",
            "history_reprocess": "📄 Выбран файл **{filename}**.\n\nВыберите одно из действий:",
            "no_history": "📭 У вас нет загруженных файлов.",
            "file_not_found": "❌ Файл не найден или был удален с сервера!",
            "lang_select": "🌐 **Выберите язык / Choose language**",
            "lang_updated": "✅ Язык успешно изменен!",
            "settings_welcome": "⚙️ **Раздел настроек**\n\nС помощью кнопки ниже вы можете изменить язык бота:",
            "choose_lang": "🌐 **Выберите язык:**",
            "settings_updated": "✅ Настройки обновлены!"
        },
        "admin": {
            "welcome": "👨‍💻 **Админ Панель**",
            "stats": "📊 **Статистика**\n\n👥 Пользователи: {total}\n📅 Активны сегодня: {today}\n📁 Файлов: {total_files}",
            "broadcast_start": "📢 Отправьте текст сообщения:",
            "broadcast_preview": "👆 Предпросмотр выше. Подтверждаете?",
            "broadcast_confirm": "✅ Рассылка началась...",
            "broadcast_done": "✅ Отправлено: {count}\n🚫 Заблокировано: {blocked}\n⚠️ Ошибок: {errors}",
            "broadcast_cancelled": "❌ Отменено."
        },
        "buttons": {
            "shuffle": "🔀 Полное перемешивание",
            "shuffle_answers": "🔀 Только ответы",
            "extract": "➕ Извлечь плюсы",
            "back": "🔙 Назад",
            "instructions_btn": "📚 Инструкция",
            "settings_btn": "⚙️ Настройки",
            "history": "📂 Мои файлы",
            "admin_panel": "👨‍💻 Админ Панель",
            "lang": "🌐 Сменить язык",
            "stats": "📊 Статистика",
            "export": "📥 Экспорт (Excel)",
            "broadcast": "📢 Рассылка",
            "confirm": "✅ Подтвердить",
            "cancel": "❌ Отмена"
        }
    },
    "en": {
        "user": {
            "welcome": "👋 **Hello! I am the Test Shuffler Bot.**\n\n"
                       "Send me a **.docx (Word)** or **.xlsx (Excel)** file with your tests.\n\n"
                       "📌 **Requirements:**\n"
                       "- File format: **.docx** or **.xlsx**\n"
                       "- Each question must be a separate block\n"
                       "- Answers must start with `+` or `=` (correct) and `-` (incorrect)",
            "wrong_ext": "❌ Please send a file in **.docx** or **.xlsx** format.",
            "too_large": "❌ File is too large (maximum 10MB).",
            "processing": "⏳ File received. Checking...",
            "success": "✅ **File saved successfully!**\n"
                       "📁 Filename: `{filename}`",
            "success_upload": "✅ **File uploaded and analyzed successfully!**\n"
                              "📊 Total questions: **{count}**.\n\n"
                              "Select one of the actions:",
            "error": "❌ File upload error: {error}",
            "instructions": "📖 **Guide:** Question starts with `?`, correct answer with `+` or `=`, incorrect with `-`.",
            "split_results": "⚠️ **Errors found!**\n\nValid: **{valid}**\nInvalid: **{invalid}**",
            "error_report_sent": "📁 Error report sent.",
            "history_welcome": "📂 **Your recent files:**",
            "history_reprocess": "📄 File **{filename}** selected.\n\nSelect one of the actions:",
            "no_history": "📭 No uploaded files found.",
            "file_not_found": "❌ File not found or has been deleted from the server!",
            "lang_select": "🌐 **Select language**",
            "lang_updated": "✅ Language updated successfully!",
            "settings_welcome": "⚙️ **Settings section**\n\nUsing the button below you can change the bot language:",
            "choose_lang": "🌐 **Select language:**",
            "settings_updated": "✅ Settings updated!"
        },
        "admin": {
            "welcome": "👨‍💻 **Admin Panel**",
            "stats": "📊 **Statistics**\n\n👥 Users: {total}\n📅 Active today: {today}\n📁 Files: {total_files}",
            "broadcast_start": "📢 Send the message text:",
            "broadcast_preview": "👆 Preview above. Confirm?",
            "broadcast_confirm": "✅ Sending started...",
            "broadcast_done": "✅ Sent: {count}\n🚫 Blocked: {blocked}\n⚠️ Errors: {errors}",
            "broadcast_cancelled": "❌ Cancelled."
        },
        "buttons": {
            "shuffle": "🔀 Full Shuffle",
            "shuffle_answers": "🔀 Shuffle Answers Only",
            "extract": "➕ Extract Pluses",
            "back": "🔙 Back",
            "instructions_btn": "📚 Guide",
            "settings_btn": "⚙️ Settings",
            "history": "📂 My Files",
            "admin_panel": "👨‍💻 Admin Panel",
            "lang": "🌐 Change Language",
            "stats": "📊 Statistics",
            "export": "📥 Export (Excel)",
            "broadcast": "📢 Broadcast",
            "confirm": "✅ Confirm",
            "cancel": "❌ Cancel"
        }
    }
}

# Errors remain unified for now or can be localized later
ERROR_TEXTS = {
    "no_questions": "❗ Faylda savollar topilmadi.",
    "missing_plus": "❗ {id}-savol: To'g'ri javob (+) belgilanmagan.",
    "few_answers": "❗ {id}-savol: Javoblar soni kam.",
    "orphan_image": "❗ {id}-qator: Rasm yoki formula savolga tegishli emas.",
    "duplicate_question": "⚠️ {id}-savol: Takroriy savol.",
    "duplicate_answer": "⚠️ {id}-savol: Javoblar bir xil.",
    "image_unattached": "❗ Question {id}: image detected but not attached to any answer or question text"
}

COMMANDS_MENU = {
    "uz": {
        "start": "♻️ Botni ishga tushirish",
        "help": "❓ Yordam va Qo'llanma",
        "admin": "👨‍💻 Admin"
    },
    "ru": {
        "start": "♻️ Запустить бота",
        "help": "❓ Помощь и инструкция",
        "admin": "👨‍💻 Админ"
    },
    "en": {
        "start": "♻️ Start the bot",
        "help": "❓ Help and Guide",
        "admin": "👨‍💻 Admin"
    }
}
