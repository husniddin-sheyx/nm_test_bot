# User Interface Texts
USER_TEXTS = {
    "welcome": "👋 Salom! Men Test Aralashtiruvchi Botman.\n"
               "Menga testlaringiz yozilgan **.docx** faylni yuboring.\n\n"
               "📌 **Talablar:**\n"
               "- Fayl formati: .docx\n"
               "- Har bir savol alohida blok bo'lishi kerak\n"
               "- Javoblar `+` (to'g'ri) va `=` (noto'g'ri) bilan boshlanishi kerak",
    "wrong_ext": "❌ Iltimos, faqat **.docx** formatidagi faylni yuboring.",
    "too_large": "❌ Fayl hajmi juda katta (maksimal 20MB).",
    "processing": "⏳ Fayl qabul qilindi. Tekshirilmoqda...",
    "success": "✅ **Fayl muvaffaqiyatli saqlandi!**\n"
               "📁 Fayl nomi: `{filename}`\n\n"
               "Endi 2-bosqich (DOCX parser) ga o'tishim mumkin.",
    "error": "❌ Faylni yuklashda xatolik yuz berdi: {error}"
}

# Admin Interface Texts (Placeholder for future)
ADMIN_TEXTS = {
    "welcome": "👨‍💻 Admin panelga xush kelibsiz.",
}

# Validation & Parser Errors
ERROR_TEXTS = {
    "no_questions": "❗ Faylda savollar topilmadi.",
    "missing_plus": "❗ {id}-savol: To'g'ri javob (+) belgilanmagan.",
    "multiple_plus": "❗ {id}-savol: {count} ta to'g'ri javob (+) belgilangan (faqat 1 ta bo'lishi kerak).",
    "few_answers": "❗ {id}-savol: Javoblar soni kam (kamida 2 ta bo'lishi kerak).",
    "orphan_image": "❗ {id}-qator: Rasm yoki formula savolga tegishli emas (context yo'q)."
}

# Buttons
BUTTONS = {
    "user": {
        "shuffle": "🔀 Aralashtirish",
        "extract": "➕ Pluslarni olish"
    },
    "admin": {
        "stats": "📊 Statistika",
        "settings": "⚙️ Sozlamalar"
    }
}
