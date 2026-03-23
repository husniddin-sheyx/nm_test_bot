# Multilingual Lexicon
LEXICON = {
    "uz": {
        "user": {
            "welcome": "👋 Salom! Men Test Aralashtiruvchi Botman.\n"
                       "Menga testlaringiz yozilgan **.docx** faylni yuboring.\n\n"
                       "📌 **Talablar:**\n"
                       "- Fayl formati: .docx\n"
                       "- Har bir savol alohida blok bo'lishi kerak\n"
                       "- Javoblar `+` yoki `=` (to'g'ri) va `-` (noto'g'ri) bilan boshlanishi kerak",
            "wrong_ext": "❌ Iltimos, faqat **.docx** formatidagi faylni yuboring.",
            "too_large": "❌ Fayl hajmi juda katta (maksimal 20MB).",
            "processing": "⏳ Fayl qabul qilindi. Tekshirilmoqda...",
            "success": "✅ **Fayl muvaffaqiyatli saqlandi!**\n"
                       "📁 Fayl nomi: `{filename}`",
            "error": "❌ Faylni yuklashda xatolik yuz berdi: {error}",
            "instructions": "📖 **Qo'llanma:** Savol `?` bilan, to'g'ri javoblar `+` yoki `=` bilan, noto'g'ri javoblar `-` bilan boshlanishi kerak.",
            "split_results": "⚠️ **Xatolar topildi!**\n\nMuvaffaqiyatli: **{valid}**\nXatoli: **{invalid}**",
            "error_report_sent": "📁 Xatolar hisoboti yuborildi.",
            "history_welcome": "📂 **Oxirgi fayllaringiz:**",
            "no_history": "📭 Sizda yuklangan fayllar yo'q.",
            "lang_select": "🌐 **Tilni tanlang / Выберите язык / Select language**",
            "lang_updated": "✅ Til muvaffaqiyatli o'zgartirildi!",
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
            "confirm": "✅ Tasdiqlash",
            "cancel": "❌ Bekor qilish"
        }
    },
    "ru": {
        "user": {
            "welcome": "👋 Привет! Я бот для перемешивания тестов.\nПришли мне файл **.docx** с вашими тестами.",
            "wrong_ext": "❌ Пожалуйста, отправьте файл в формате **.docx**.",
            "too_large": "❌ Файл слишком большой (макс. 20МБ).",
            "processing": "⏳ Файл получен. Проверяю...",
            "success": "✅ **Файл успешно сохранен!**\n📁 Имя файла: `{filename}`",
            "error": "❌ Ошибка при загрузке: {error}",
            "instructions": "📖 **Инструкция:** Вопрос начинается с `?`, правильный ответ с `+`, неправильный с `-` или `=`.",
            "split_results": "⚠️ **Найдены ошибки!**\n\nУспешно: **{valid}**\nС ошибками: **{invalid}**",
            "error_report_sent": "📁 Отчет об ошибках отправлен.",
            "history_welcome": "📂 **Ваши последние файлы:**",
            "no_history": "📭 У вас нет загруженных файлов.",
            "lang_select": "🌐 **Выберите язык**",
            "lang_updated": "✅ Язык успешно изменен!",
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
            "confirm": "✅ Подтвердить",
            "cancel": "❌ Отмена"
        }
    },
    "en": {
        "user": {
            "welcome": "👋 Hello! I am the Test Shuffler Bot.\nSend me a **.docx** file with your tests.",
            "wrong_ext": "❌ Please send a file in **.docx** format.",
            "too_large": "❌ File is too large (max 20MB).",
            "processing": "⏳ File received. Checking...",
            "success": "✅ **File saved successfully!**\n📁 Filename: `{filename}`",
            "error": "❌ File upload error: {error}",
            "instructions": "📖 **Guide:** Question starts with `?`, correct answer with `+`, incorrect with `-` or `=`.",
            "split_results": "⚠️ **Errors found!**\n\nValid: **{valid}**\nInvalid: **{invalid}**",
            "error_report_sent": "📁 Error report sent.",
            "history_welcome": "📂 **Your recent files:**",
            "no_history": "📭 No uploaded files found.",
            "lang_select": "🌐 **Select language**",
            "lang_updated": "✅ Language updated successfully!",
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
    "duplicate_answer": "⚠️ {id}-savol: Javoblar bir xil."
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
