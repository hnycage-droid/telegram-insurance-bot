from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler, ContextTypes

# القائمة الرئيسية
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🚗 تأمين السيارات", callback_data='auto')],
        [InlineKeyboardButton("🏠 تأمين الحريق والممتلكات", callback_data='fire')],
        [InlineKeyboardButton("📦 تأمين النقل البري و البحري ", callback_data='shipping')],
        [InlineKeyboardButton("📦 تأمين الحياة ", callback_data='life')],
        [InlineKeyboardButton("📦 التأمين الصحي ", callback_data='health')],
        [InlineKeyboardButton("📦 الملف التعريفي بالشركة ", callback_data='prof')],
        [InlineKeyboardButton("📞 التواصل معنا", callback_data='contact')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = (
        "مرحباً بك في الشركة الاسلامية السورية للتأمين! 🛡️\n"
        "يسرنا تقديم حلول تأمينية متكاملة لحمايتك وحماية أعمالك.\n"
        "اختر أحد الخيارات التالية للاطلاع على التفاصيل:"
    )
    
    if update.message:
        await update.message.reply_text(text, reply_markup=reply_markup)
    else:
        await update.callback_query.message.edit_text(text, reply_markup=reply_markup)

# الاستجابة للضغط على الأزرار
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    back_button = [[InlineKeyboardButton("🔙 العودة للقائمة الرئيسية", callback_data='main_menu')]]
    
    if query.data == 'auto':
        msg = (
            "🚗 *تأمين السيارات*\n\n"
            "• تغطية الشامل وضد الغير بأفضل الأسعار.\n"
            "• إصلاح داخل الوكالة أو الورش المعتمدة.\n"
            "• خدمة المساعدة على الطريق وتوفير سيارة بديلة."
        )
    elif query.data == 'fire':
        msg = (
            "🏠 *تأمين الحريق والممتلكات*\n\n"
            "• حماية كاملة للمنشآت التجارية و الصناعية والمنازل ضد أخطار الحريق والتلف.\n"
            "• تغطية السرقة والتماس الكهربائي، والانفجار."
            "• تغطية اخطار الطبيعة."
        )
    elif query.data == 'life':
        msg = (
            "🏠 *تأمين الأفراد والمجموعات*\n\n"
            "• في حالة الوفاة لأي سبب.\n"
            "• العجز الكلي و الجزئي."
            "• تغطية اخطار الطبيعة."
        )
    elif query.data == 'health':
        msg = (
            "🏠 *تأمين الأفراد والمجموعات*\n\n"
            "• داخل المشفى للعمليات الباردة و الاسعافية.\n"
            "• خارج المشفى زيارة الطبيب."
            "• التصوير الشعاعي والمخابر والادوية."
        )
    elif query.data == 'shipping':
        msg = (
            "📦 *تأمين البضائع (Express Shipping)*\n\n"
            "• وحماية الشحنات والبضائع أثناء النقل البري، البحري، والجوّي.\n"
            "• تعويض سريع في حالات الفقدان، التلف، أو الحوادث الطارئة."
        )
    elif query.data == 'prof':
        msg = (
            "📦 *اضغط على الرابط (Express Shipping)*\n\n"
            "• للاطلاع على الملف التعريفي للشركة.\n"
            "• https://siic-insurance.com/SIICProfilev1.pdf"
        )
    elif query.data == 'contact':
        msg = (
            "📞 *معلومات التواصل والدعم الفني*\n\n"
            "• 📱 *المركز الرئيسي:* 00963119795\n"
            "• ✉️ *البريد الإلكتروني:* info@siic-insurance.com\n"
            "• 💬 *المحادثة المباشرة:* @hgeca\n"
            "• 🌐 *الموقع الإلكتروني:* www.siic-insurance.com"
        )
    elif query.data == 'main_menu':
        await start(update, context)
        return

    await query.edit_message_text(
        text=msg, 
        parse_mode='Markdown', 
        reply_markup=InlineKeyboardMarkup(back_button)
    )

if __name__ == '__main__':
    # استبدل TOKEN بالرمز الخاص ببوتك من BotFather
    app = ApplicationBuilder().token("8871716550:AAEzAdvXcyLwT0W0N2z6fH1ve-d6VDzfwJ4").build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_click))
    
    app.run_polling()
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
    ContextTypes,
    filters
)

# تعريف مراحل المحادثة (Conversation States)
NAME, POLICY_NUM, INCIDENT_DESC, PHOTO = range(4)

# ضع هنا معرف Chat ID الخاص بك أو بمجموعة موظفي التأمين لتلقي البلاغات
ADMIN_CHAT_ID = "@Hgeca"

# 1. بدء استقبال البلاغ
async def start_claim(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query:
        await query.answer()
        await query.message.reply_text("📝 *بدء تقديم بلاغ / طلب جديد*\n\nالرجاء إدخال اسمك الكامل:", parse_mode='Markdown')
    else:
        await update.message.reply_text("📝 *بدء تقديم بلاغ / طلب جديد*\n\nالرجاء إدخال اسمك الكامل:", parse_mode='Markdown')
    return NAME

# 2. استلام الاسم وطلب رقم الوثيقة
async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['name'] = update.message.text
    await update.message.reply_text("شكراً لك. يرجى إدخال رقم وثيقة التأمين (أو اكتب 'عميل جديد'):")
    return POLICY_NUM

# 3. استلام رقم الوثيقة وطلب التفاصيل
async def get_policy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['policy'] = update.message.text
    await update.message.reply_text("يرجى شرح أسباب الطلب أو تفاصيل الحادث بالتفصيل:")
    return INCIDENT_DESC

# 4. استلام التفاصيل وطلب صورة المرفقات
async def get_desc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['desc'] = update.message.text
    await update.message.reply_text("يرجى إرسال صورة الحادث/الأوراق، أو قم بكتابة 'تخطي' للاستمرار بدون صورة:")
    return PHOTO

# 5. استلام الصورة (إن وجدت) وإرسال البلاغ للفريق
async def get_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = context.user_data
    
    if update.message.photo:
        photo_file_id = update.message.photo[-1].file_id
        photo_note = "تم إرفاق صورة 📷"
    else:
        photo_file_id = None
        photo_note = "لم يتم إرفاق صورة."

    # صياغة الرسالة الموجهة للإدارة
    summary = (
        "🚨 *بلاغ جديد متلقى عبر البوت*\n\n"
        f"👤 *الاسم:* {user_data.get('name')}\n"
        f"📄 *رقم الوثيقة:* {user_data.get('policy')}\n"
        f"📝 *التفاصيل:* {user_data.get('desc')}\n"
        f"🖼️ *المرفقات:* {photo_note}\n"
        f"📲 *حساب المرسل:* @{update.effective_user.username or 'غير محدد'} (ID: {update.effective_user.id})"
    )

    # تحويل البلاغ إلى قناة أو حساب الإدارة
    if photo_file_id:
        await context.bot.send_photo(chat_id=ADMIN_CHAT_ID, photo=photo_file_id, caption=summary, parse_mode='Markdown')
    else:
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=summary, parse_mode='Markdown')

    await update.message.reply_text("✅ *تم استلام بلاغك بنجاح!*\nسيقوم فريق المطالبات بالتواصل معك قريباً.", parse_mode='Markdown')
    return ConversationHandler.END

# إلغاء العملية
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("تم إلغاء تقديم البلاغ.")
    return ConversationHandler.END

# إعداد الموجهات (Handlers)
claim_handler = ConversationHandler(
    entry_points=[
        CommandHandler('claim', start_claim),
        CallbackQueryHandler(start_claim, pattern='^claim$')
    ],
    states={
        NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
        POLICY_NUM: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_policy)],
        INCIDENT_DESC: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_desc)],
        PHOTO: [
            MessageHandler(filters.PHOTO, get_photo),
            MessageHandler(filters.TEXT & ~filters.COMMAND, get_photo)
        ],
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)

if __name__ == '__main__':
    app = ApplicationBuilder().token("8871716550:AAEzAdvXcyLwT0W0N2z6fH1ve-d6VDzfwJ4").build()
    app.add_handler(claim_handler)
    app.run_polling()
