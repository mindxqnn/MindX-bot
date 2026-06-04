# =====================================
# MINDX COMMUNITY BOT
# =====================================

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
import google.generativeai as genai
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    CallbackQueryHandler, filters, ContextTypes
)

# ⚠️ ӨӨРИЙНХӨӨРӨӨ СОЛИНО УУ
TOKEN = "8820335390:AAHzpsGQRwVtSArZvIg-EDJo8_o0FHAsVXo"
ADMIN_ID = 1983266908  # Таны Telegram ID (https://t.me/userinfobot-оос авна)
GROQ_KEY = "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"

# MindX холбоосууд - өөрийнхөөрөө солино уу
MINDX_CHANNEL = "https://t.me/MindXbrothers"
MINDX_GROUP = "https://www.facebook.com/share/g/1E7rhyTdZE/"
MINDX_WEBSITE = "https://mindxhub.com/"
DERIV_LINK = "https://track.deriv.com/_yGETkDh0KKMKqFKZ7JdnQ2Nd7ZgqdRLk/1/"

# =====================================
# ХЭРЭГСЛИЙН ФУНКЦУУД
# =====================================

def is_admin(user_id: int) -> bool:
    return user_id == ADMIN_ID

# =====================================
# ГИШҮҮНИЙ КОМАНДУУД
# =====================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    keyboard = [
        [InlineKeyboardButton("MindX-д нэгдэх", callback_data="join")],
        [InlineKeyboardButton("Чаннел", url=MINDX_CHANNEL),
         InlineKeyboardButton("Групп", url=MINDX_GROUP)],
        [InlineKeyboardButton("Вэбсайт", url=MINDX_WEBSITE)],
        [InlineKeyboardButton("Deriv дансаа нээх", url=DERIV_LINK)],
        [InlineKeyboardButton("Бидний тухай", callback_data="about")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"Сайн уу, {user.first_name}! 👋\n\n"
        f"*MindX Community*-д тавтай морил!\n\n"
        f"Бид арилжааны чиглэлээр мэдлэг, мэдээлэл хуваалцдаг коммунити.\n\n"
        f"Доорх товчнуудаас сонгоно уу 👇",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def join_guide(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Чаннелд нэгдэх", url=MINDX_CHANNEL)],
        [InlineKeyboardButton("Группд нэгдэх", url=MINDX_GROUP)],
        [InlineKeyboardButton("Буцах", callback_data="back_start")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = (
        "📋 *MindX-д хэрхэн нэгдэх вэ?*\n\n"
        "1️⃣ Доорх *Чаннелд нэгдэх* товч дарна\n"
        "2️⃣ Telegram нээгдэж чаннел харагдана\n"
        "3️⃣ *Join* товч дарж нэгдэнэ\n"
        "4️⃣ Мөн *Группд нэгдэх* товчоор группт орно\n\n"
        "✅ Бүгдийг хийсний дараа та MindX-ийн гишүүн боллоо!"
    )
    if update.callback_query:
        await update.callback_query.edit_message_text(text, reply_markup=reply_markup, parse_mode="Markdown")
    else:
        await update.message.reply_text(text, reply_markup=reply_markup, parse_mode="Markdown")

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("Буцах", callback_data="back_start")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = (
        "🏢 *MindX Community гэж юу вэ?*\n\n"
        "MindX бол арилжааны чиглэлээр:\n"
        "• Мэдлэг хуваалцдаг\n"
        "• Мэдээлэл тараадаг\n"
        "• Хамтдаа ургадаг\n\n"
        "коммунити юм.\n\n"
        f"🌐 Вэбсайт: {MINDX_WEBSITE}"
    )
    if update.callback_query:
        await update.callback_query.edit_message_text(text, reply_markup=reply_markup, parse_mode="Markdown")
    else:
        await update.message.reply_text(text, reply_markup=reply_markup, parse_mode="Markdown")

async def links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Чаннел", url=MINDX_CHANNEL)],
        [InlineKeyboardButton("Групп", url=MINDX_GROUP)],
        [InlineKeyboardButton("Вэбсайт", url=MINDX_WEBSITE)],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "🔗 *MindX холбоосууд*\n\nДоорх товчнуудаас нэвтэрнэ үү:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# =====================================
# АДМИНЫ КОМАНДУУД
# =====================================

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.message.from_user.id):
        await update.message.reply_text("❌ Зөвхөн админ ашиглах боломжтой.")
        return

    if not context.args:
        await update.message.reply_text(
            "📢 Мэдээлэл тараахдаа:\n\n"
            "/broadcast Энд мэдэгдэлээ бичнэ\n\n"
            "Жишээ:\n"
            "/broadcast Өнөөдөр 8 цагт арилжааны сургалт болно!"
        )
        return

    msg = " ".join(context.args)
    broadcast_text = f"📢 *MindX мэдэгдэл*\n\n{msg}"

    await update.message.reply_text(
        f"✅ Мэдэгдэл илгээгдлээ:\n\n{broadcast_text}",
        parse_mode="Markdown"
    )

async def send_invite(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.message.from_user.id):
        await update.message.reply_text("❌ Зөвхөн админ ашиглах боломжтой.")
        return

    keyboard = [
        [InlineKeyboardButton("Чаннелд нэгдэх", url=MINDX_CHANNEL)],
        [InlineKeyboardButton("Группд нэгдэх", url=MINDX_GROUP)],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "🎉 *MindX Community-д урьж байна!*\n\n"
        "Арилжааны чиглэлээр мэдлэг хуваалцдаг манай коммунитид нэгдээрэй.\n\n"
        "Доорх товч дарж нэгдэнэ үү 👇",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def share_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.message.from_user.id):
        await update.message.reply_text("❌ Зөвхөн админ ашиглах боломжтой.")
        return
    await update.message.reply_text(
        "📎 Файл хуваалцахдаа:\n\n"
        "Файлаа шууд botд илгээгээрэй — би гишүүдэд дамжуулна.\n\n"
        "Одоогоор файлаа илгээнэ үү."
    )

async def admin_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.message.from_user.id):
        await update.message.reply_text("❌ Зөвхөн админ ашиглах боломжтой.")
        return
    await update.message.reply_text(
        "⚙️ *Админы командууд*\n\n"
        "/broadcast [текст] — Мэдэгдэл тараах\n"
        "/invite — Урилгын товчлуур илгээх\n"
        "/sharefile — Файл хуваалцах\n"
        "/adminhelp — Энэ жагсаалт\n",
        parse_mode="Markdown"
    )

# =====================================
# ТОВЧЛУУРЫН ХАРИУ
# =====================================

async def ai_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text
    await update.message.reply_text("Бодож байна...")
    try:
        import requests
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {GROQ_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": "Та MindX арилжааны коммунитийн туслах AI байна. Хэрэглэгч латин үсгээр галиглаж бичсэн монгол үгийг ойлгоод асуултад нь ХАРИУЛНА. Хариултаа кирилл монгол хэлээр бич. Хэзээ ч галиглалыг зүгээр хөрвүүлж болохгүй — заавал утга бүхий хариулт өгнө."},
                {"role": "user", "content": user_msg}
            ]
        }
        r = requests.post(url, headers=headers, json=data)
        answer = r.json()["choices"][0]["message"]["content"]
        await update.message.reply_text(answer)
    except Exception as e:
        await update.message.reply_text(f"Алдаа: {str(e)}")
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "join":
        await join_guide(update, context)
    elif query.data == "about":
        await about(update, context)
    elif query.data == "back_start":
        keyboard = [
            [InlineKeyboardButton("MindX-д нэгдэх", callback_data="join")],
            [InlineKeyboardButton("Чаннел", url=MINDX_CHANNEL),
             InlineKeyboardButton("Групп", url=MINDX_GROUP)],
            [InlineKeyboardButton("Вэбсайт", url=MINDX_WEBSITE)],
            [InlineKeyboardButton("Бидний тухай", callback_data="about")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "MindX Community-д тавтай морил!\n\nДоорх товчнуудаас сонгоно уу 👇",
            reply_markup=reply_markup
        )

# =====================================
# ШИНЭ ГИШҮҮН МЭНДЛЭХ
# =====================================

async def welcome_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        if member.is_bot:
            continue
        keyboard = [
            [InlineKeyboardButton("Дүрэм журам", callback_data="about")],
            [InlineKeyboardButton("Чаннел", url=MINDX_CHANNEL)],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            f"👋 Сайн уу, {member.first_name}!\n\n"
            f"*MindX Community*-д тавтай морил!\n\n"
            f"Бид арилжааны мэдлэг хуваалцдаг коммунити.\n"
            f"Чаннелд нэгдэж мэдээлэл авна уу 👇",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )

# =====================================
# БОТЫГ ЭХЛҮҮЛЭХ
# =====================================

if __name__ == "__main__":
    print("MindX бот эхэллээ... Зогсоохдоо Ctrl+C дар")
    app = ApplicationBuilder().token(TOKEN).build()

    # Гишүүний командууд
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("join", join_guide))
    app.add_handler(CommandHandler("links", links))
    app.add_handler(CommandHandler("about", about))
    
    # Админы командууд
    app.add_handler(CommandHandler("broadcast", broadcast))
    app.add_handler(CommandHandler("invite", send_invite))
    app.add_handler(CommandHandler("sharefile", share_file))
    app.add_handler(CommandHandler("adminhelp", admin_help))

    # Товчлуур & шинэ гишүүн
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_new_member))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ai_chat))

    app.run_polling()
