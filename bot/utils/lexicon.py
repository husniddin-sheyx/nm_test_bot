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
    "error": "❌ Faylni yuklashda xatolik yuz berdi: {error}",
    "instructions": "📖 **Botdan foydalanish bo'yicha batafsil qo'llanma:**\n\n"
                    "1. **Faylni tayyorlash:**\n"
                    "   - Savollarni `.docx` formatidagi faylga yozing.\n"
                    "   - Savol: `?` bilan boshlanadi. Savol matni bir necha qatordan iborat bo'lishi mumkin.\n"
                    "   - To'g'ri javob: `+` bilan boshlanadi.\n"
                    "   - Noto'g'ri javob: `-` yoki `=` bilan boshlanadi.\n"
                    "   - **Rasmlar/Formulalar**: Ularni aynan o'sha savol yoki javob matnidan keyin joylashtiring. Bot ularni o'z joyida saqlab qoladi.\n\n"
                    "2. **Faylni yuborish:**\n"
                    "   - Tayyor faylni botga tashlang. Bot avtomatik tekshirib chiqadi.\n\n"
                    "3. **Xatolarni boshqarish:**\n"
                    "   - Agar faylda xatolar bo'lsa, bot sizga batafsil **Xatolar hisoboti**ni yuboradi.\n"
                    "   - Hisoboti faylini ochib, xatolarni tuzatib, qayta yuborishingiz mumkin.\n\n"
                    "4. **Natijani olish:**\n"
                    "   - **To'liq aralashtirish**: Savollar va javoblar tartibi o'zgaradi.\n"
                    "   - **Faqat javoblar**: Savollar tartibi saqlanadi, faqat variantlar aralashadi.\n"
                    "   - **Pluslarni olish**: Faqat to'g'ri javoblar qoladi (shpargalka uchun).",
    "split_results": "⚠️ **Faylda ayrim xatolar topildi!**\n\n"
                     "Muvaffaqiyatli tekshirilgan savollar: **{valid}** ta.\n"
                     "Xatosi bor savollar: **{invalid}** ta.\n\n"
                     "Siz muvaffaqiyatli savollarni qayta ishlashingiz mumkin. Xatolar esa alohida faylda yuborildi.",
    "error_report_sent": "📁 **Xatolar hisoboti yuborildi.** Iltimos, ushbu faylni ochib, xatolarni tuzating va qayta yuboring."
}

# Admin Interface Texts (Placeholder for future)
ADMIN_TEXTS = {
    "welcome": "👨‍💻 **Admin Panel (V5.0)**\n\nQuyidagi tugmalar orqali botni boshqarishingiz mumkin:",
    "stats": "📊 **Bot Statistikasi**\n\n"
             "👥 Jami: **{total}** ta\n"
             "📅 Bugun faol: **{today}** ta\n"
             "🗓 Haftalik faol: **{week}** ta",
    "broadcast_start": "📢 Hammaga yuboriladigan xabarni yozing (matn, rasm, video...):",
    "broadcast_preview": "👆 **Xabar ko'rinishi yuqorida.**\n\nUni barcha foydalanuvchilarga yuborishni tasdiqlaysizmi?",
    "broadcast_confirm": "✅ Xabar yuborish boshlandi...",
    "broadcast_done": "✅ Xabar yuborildi!\n\n"
                     "Yuborildi: {count} ta\n"
                     "Bloklaganlar: {blocked} ta",
    "broadcast_cancelled": "❌ Xabar yuborish bekor qilindi."
}

# Validation & Parser Errors
ERROR_TEXTS = {
    "no_questions": "❗ Faylda savollar topilmadi.",
    "missing_plus": "❗ {id}-savol: To'g'ri javob (+) belgilanmagan.",
    "multiple_plus": "❗ {id}-savol: {count} ta to'g'ri javob (+) belgilangan (faqat 1 ta bo'lishi kerak).",
    "few_answers": "❗ {id}-savol: Javoblar soni kam (kamida 2 ta bo'lishi kerak).",
    "orphan_image": "❗ {id}-qator: Rasm yoki formula savolga tegishli emas (context yo'q).",
    "duplicate_question": "⚠️ {id}-savol: Bu savol matni avvalroq ({first_id}-savol) ham ishlatilgan. (Takroriy savol)",
    "duplicate_answer": "⚠️ {id}-savol: Quyidagi javoblar bir xil: {dupes}"
}

# Buttons
BUTTONS = {
    "user": {
        "shuffle": "🔀 To'liq Aralashtirish",
        "shuffle_answers": "🔀 Faqat javoblar",
        "extract": "➕ Pluslarni olish",
        "back": "🔙 Boshiga qaytish",
        "instructions_btn": "📚 Qo'llanma",
        "settings_btn": "⚙️ Sozlamalar",
        "admin_panel": "👨‍💻 Admin Panel"
    },
    "admin": {
        "stats": "📊 Statistika",
        "broadcast": "📢 Xabar yuborish",
        "export": "📁 Excel yuklab olish",
        "back": "🔙 Orqaga",
        "confirm": "✅ Tasdiqlash",
        "cancel": "❌ Bekor qilish"
    }
}

COMMANDS_MENU = {
    "start": "♻️ Botni ishga tushirish",
    "help": "❓ Yordam va Qo'llanma",
    "admin": "👨‍💻 Admin Panelga kirish"
}
