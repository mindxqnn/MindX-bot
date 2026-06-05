# =====================================
# MINDX COMMUNITY BOT
# =====================================

import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    CallbackQueryHandler, filters, ContextTypes
)

TOKEN = os.environ.get("TOKEN")
ADMIN_ID = int(os.environ.get("ADMIN_ID", "0"))
GROQ_KEY = os.environ.get("GROQ_KEY")

MINDX_CHANNEL = "https://t.me/MindXbrothers"
MINDX_FACEBOOK_GROUP = "https://www.facebook.com/share/g/18nY4wdSqm/"
MINDX_FACEBOOK_PAGE = "https://www.facebook.com/official.MindX/"
MINDX_INSTAGRAM = "https://www.instagram.com/mindx.official/"
MINDX_WHATSAPP = "https://chat.whatsapp.com/GGYJiQlEij2IlTtdWRR1rc?mode=gi_t"
MINDX_WEBSITE = "https://mindxhub.com/"
DERIV_LINK = "https://track.deriv.com/_yGETkDh0KKMKqFKZ7JdnQ2Nd7ZgqdRLk/1/"

# Хэлний текстүүд
TEXTS = {
    "mn": {
        "welcome": "Сайн уу, {name}! 👋\n\n*MindX Community*-д тавтай морил!\n\nБид арилжааны чиглэлээр мэдлэг, мэдээлэл хуваалцдаг коммунити.\n\nДоорх товчнуудаас сонгоно уу 👇",
        "join": "MindX-д нэгдэх",
        "social": "🌐 MindX Social",
        "website": "Вэбсайт",
        "deriv": "Deriv дансаа нээх",
        "contact": "Админтай холбогдох",
        "about": "Бидний тухай",
        "language": "🌐 English",
        "join_text": "📋 *MindX-д хэрхэн нэгдэх вэ?*\n\n1️⃣ Доорх *Telegram* товч дарна\n2️⃣ Telegram нээгдэж чаннел харагдана\n3️⃣ *Join* товч дарж нэгдэнэ\n\n✅ Бүгдийг хийсний дараа та MindX-ийн гишүүн боллоо!",
        "telegram_btn": "✈️ Telegram",
        "back": "Буцах",
        "social_text": "🌐 *MindX Social*\n\nМанайд нэгдэж, хамт урагшилцгаая! 👇",
        "contact_text": "📞 *Админтай холбогдох*\n\nДоорх товчнуудаар шууд холбогдоно уу:",
        "about_text": "🏢 *MindX Community гэж юу вэ?*\n\nMindX бол арилжааны чиглэлээр:\n• Мэдлэг хуваалцдаг\n• Мэдээлэл тараадаг\n• Хамтдаа ургадаг\n\nкоммунити юм.\n\n🌐 Вэбсайт: {website}",
        "thinking": "Бодож байна...",
        "welcome_new": "👋 Сайн уу, {name}!\n\n*MindX Community*-д тавтай морил!\n\nЧаннелд нэгдэж мэдээлэл авна уу 👇",
    },
    "en": {
        "welcome": "Hello, {name}! 👋\n\nWelcome to *MindX Community*!\n\nWe are a community that shares knowledge and information about trading.\n\nChoose from the options below 👇",
        "join": "Join MindX",
        "social": "🌐 MindX Social",
        "website": "Website",
        "deriv": "Open Deriv Account",
        "contact": "Contact Admin",
        "about": "About Us",
        "language": "🌐 Монгол",
        "join_text": "📋 *How to join MindX?*\n\n1️⃣ Click the *Telegram* button below\n2️⃣ Telegram will open and show the channel\n3️⃣ Press *Join* to become a member\n\n✅ After completing these steps, you are a MindX member!",
        "telegram_btn": "✈️ Telegram",
        "back": "Back",
        "social_text": "🌐 *MindX Social*\n\nJoin us and grow together! 👇",
        "contact_text": "📞 *Contact Admin*\n\nReach out directly through the buttons below:",
        "about_text": "🏢 *What is MindX Community?*\n\nMindX is a community that:\n• Shares knowledge\n• Distributes information\n• Grows together\n\nabout trading.\n\n🌐 Website: {website}",
        "thinking": "Thinking...",
        "welcome_new": "👋 Hello, {name}!\n\nWelcome to *MindX Community*!\n\nJoin our channel to get updates 👇",
    }
}

user_lang = {}

def get_lang(user_id):
    return user_lang.get(user_id, "mn")

def get_text(user_id, key, **kwargs):
    lang = get_lang(user_id)
    text = TEXTS[lang].get(key, "")
    return text.format(**kwargs) if kwargs else text

def is_admin(user_id: int) -> bool:
    return user_id == ADMIN_ID

def main_keyboard(user_id):
    t = TEXTS[get_lang(user_id)]
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(t["join"], url=MINDX_CHANNEL)],
        [InlineKeyboardButton(t["social"], callback_data="social")],
        [InlineKeyboardButton(t["website"], url=MINDX_WEBSITE)],
        [InlineKeyboardButton(t["deriv"], url=DERIV_LINK)],
        [InlineKeyboardButton(t["contact"], callback_data="contact")],
        [InlineKeyboardButton(t["about"], callback_data="about")],
        [InlineKeyboardButton(t["language"], callback_data="lang")],
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    await update.message.reply_text(
        get_text(user.id, "welcome", name=user.first_name),
        reply_markup=main_keyboard(user.id),
        parse_mode="Markdown"
    )

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id if update.message else update.callback_query.from_user.id
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(get_text(user_id, "back"), callback_data="back_start")]])
    text = get_text(user_id, "about_text", website=MINDX_WEBSITE)
    if update.callback_query:
        await update.callback_query.edit_message_text(text, reply_markup=keyboard, parse_mode="Markdown")
    else:
        await update.message.reply_text(text, reply_markup=keyboard, parse_mode="Markdown")

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.message.from_user.id):
        await update.message.reply_text("❌ Зөвхөн админ ашиглах боломжтой.")
        return
    if not context.args:
        await update.message.reply_text("/broadcast Энд мэдэгдэлээ бичнэ")
        return
    msg = " ".join(context.args)
    await update.message.reply_text(f"📢 *MindX мэдэгдэл*\n\n{msg}", parse_mode="Markdown")

async def send_invite(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.message.from_user.id):
        await update.message.reply_text("❌ Зөвхөн админ ашиглах боломжтой.")
        return
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("✈️ Telegram", url=MINDX_CHANNEL)]])
    await update.message.reply_text(
        "🎉 *MindX Community-д урьж байна!*\n\nДоорх товч дарж нэгдэнэ үү 👇",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

async def admin_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.message.from_user.id):
        await update.message.reply_text("❌ Зөвхөн админ ашиглах боломжтой.")
        return
    await update.message.reply_text(
        "⚙️ *Админы командууд*\n\n"
        "/broadcast [текст] — Мэдэгдэл тараах\n"
        "/invite — Урилгын товчлуур илгээх\n"
        "/adminhelp — Энэ жагсаалт\n",
        parse_mode="Markdown"
    )

async def ai_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_msg = update.message.text
    await update.message.reply_text(get_text(user_id, "thinking"))
    try:
        import requests
        lang = get_lang(user_id)
        system_prompt = (
            "You are MindX community's AI assistant. Reply in English only."
            if lang == "en"
            else "Та MindX арилжааны коммунитийн туслах AI байна. Хэрэглэгч монгол үгийг латин үсгээр галиглаж бичиж болно. Тэдгээрийг монгол кирилл үг гэж ойлгоод кирилл монгол хэлээр хариулна уу. Хариултаа ЗӨВХӨН кирилл монгол үсгээр бич."
        )
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"}
        data = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_msg}
            ]
        }
        r = requests.post(url, headers=headers, json=data)
        answer = r.json()["choices"][0]["message"]["content"]
        await update.message.reply_text(answer)
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()
    t = TEXTS[get_lang(user_id)]

    if query.data == "lang":
        user_lang[user_id] = "en" if get_lang(user_id) == "mn" else "mn"
        t = TEXTS[get_lang(user_id)]
        await query.edit_message_text(
            t["welcome"].format(name=query.from_user.first_name),
            reply_markup=main_keyboard(user_id),
            parse_mode="Markdown"
        )
    elif query.data == "join":
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(t["telegram_btn"], url=MINDX_CHANNEL)],
            [InlineKeyboardButton(t["back"], callback_data="back_start")],
        ])
        await query.edit_message_text(t["join_text"], reply_markup=keyboard, parse_mode="Markdown")
    elif query.data == "social":
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("✈️ Telegram", url=MINDX_CHANNEL)],
            [InlineKeyboardButton("👥 Facebook Group", url=MINDX_FACEBOOK_GROUP)],
            [InlineKeyboardButton("📘 Facebook Page", url=MINDX_FACEBOOK_PAGE)],
            [InlineKeyboardButton("📸 Instagram", url=MINDX_INSTAGRAM)],
            [InlineKeyboardButton("💬 WhatsApp", url=MINDX_WHATSAPP)],
            [InlineKeyboardButton(t["back"], callback_data="back_start")],
        ])
        await query.edit_message_text(t["social_text"], reply_markup=keyboard, parse_mode="Markdown")
    elif query.data == "contact":
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("👤 Admin 1 - @Big_qnn", url="https://t.me/Big_qnn")],
            [InlineKeyboardButton("👤 Admin 2 - @G_Boggi", url="https://t.me/G_Boggi")],
            [InlineKeyboardButton(t["back"], callback_data="back_start")],
        ])
        await query.edit_message_text(t["contact_text"], reply_markup=keyboard, parse_mode="Markdown")
    elif query.data == "about":
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(t["back"], callback_data="back_start")]])
        await query.edit_message_text(
            t["about_text"].format(website=MINDX_WEBSITE),
            reply_markup=keyboard,
            parse_mode="Markdown"
        )
    elif query.data == "back_start":
        await query.edit_message_text(
            t["welcome"].format(name=query.from_user.first_name),
            reply_markup=main_keyboard(user_id),
            parse_mode="Markdown"
        )

async def welcome_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        if member.is_bot:
            continue
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("✈️ Telegram", url=MINDX_CHANNEL)]])
        await update.message.reply_text(
            f"👋 Сайн уу, {member.first_name}!\n\n*MindX Community*-д тавтай морил!\n\nЧаннелд нэгдэж мэдээлэл авна уу 👇",
            reply_markup=keyboard,
            parse_mode="Markdown"
        )

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"MindX Bot Running!")
    def log_message(self, format, *args):
        pass

def run_server():
    HTTPServer(("0.0.0.0", 8080), Handler).serve_forever()

if __name__ == "__main__":
    print("MindX бот эхэллээ... Зогсоохдоо Ctrl+C дар")
    threading.Thread(target=run_server, daemon=True).start()
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("about", about))
    app.add_handler(CommandHandler("broadcast", broadcast))
    app.add_handler(CommandHandler("invite", send_invite))
    app.add_handler(CommandHandler("adminhelp", admin_help))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_new_member))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ai_chat))
    app.run_polling()
