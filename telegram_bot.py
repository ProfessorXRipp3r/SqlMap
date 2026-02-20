import os
import asyncio
import re
from collections import defaultdict
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

user_sessions = defaultdict(lambda: {'url': None, 'options': set(), 'page': 0, 'session_id': None})

ALL_OPTIONS = [
    {'Databases': '--dbs', 'Tables': '--tables', 'Columns': '--columns', 'Dump All': '--dump-all'},
    {'Current DB': '--current-db', 'Current User': '--current-user', 'Hostname': '--hostname', 'Passwords': '--passwords'},
]

def create_keyboard(user_id, page=0):
    keyboard = []
    options = ALL_OPTIONS[page]
    
    row = []
    for label, value in options.items():
        session = user_sessions[user_id]
        prefix = "✅ " if value in session['options'] else ""
        row.append(InlineKeyboardButton(f"{prefix}{label}", callback_data=f"opt_{page}_{label}"))
        if len(row) == 2:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
    
    nav_row = []
    if page > 0:
        nav_row.append(InlineKeyboardButton("◀️ Previous", callback_data=f"page_{page-1}"))
    if page < len(ALL_OPTIONS) - 1:
        nav_row.append(InlineKeyboardButton("Next ▶️", callback_data=f"page_{page+1}"))
    if nav_row:
        keyboard.append(nav_row)
    
    keyboard.append([InlineKeyboardButton("✔️ Done", callback_data="done")])
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔰 SQLMap Bot\n\n"
        "Commands:\n"
        "• /sqlmap <URL> - Start scan\n"
    )

async def sqlmap_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if not context.args:
        await update.message.reply_text("❌ Usage: /sqlmap http://target.com?id=1")
        return
    
    url = context.args[0]
    if not re.match(r'https?://', url):
        await update.message.reply_text("❌ Invalid URL")
        return
    
    session_id = re.sub(r'[^a-zA-Z0-9]', '_', url)[:50]
    user_sessions[user_id] = {'url': url, 'options': set(), 'page': 0, 'session_id': session_id}
    
    await update.message.reply_text(
        f"🌐 Target: `{url}`\n\n**Page 1/{len(ALL_OPTIONS)}**",
        reply_markup=create_keyboard(user_id, 0),
        parse_mode='Markdown'
    )

def main():
    token = os.getenv('TELEGRAM_TOKEN')
    if not token:
        print("Error: TELEGRAM_TOKEN not set")
        exit(1)
    
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("sqlmap", sqlmap_cmd))
    
    print("Bot started")
    app.run_polling()

if __name__ == "__main__":
    main()
