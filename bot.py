import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes

# Bot Token - Render.com Environment Variable එකෙන් ගන්න
BOT_TOKEN = os.environ.get("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
# Web App URL - Render.com එකෙන් ලැබෙන URL එක (Automatic)
WEBAPP_URL = os.environ.get("WEBAPP_URL", "https://your-app.onrender.com")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/start command - Auto link එක generate කරලා එවනවා"""
    user = update.effective_user
    user_id = user.id
    first_name = user.first_name or "User"
    
    # Unique link එක හදනවා (user ID එක එක්ක)
    unique_link = f"{WEBAPP_URL}/loc/?id={user_id}"
    
    # ලස්සන message එක + Web App Button එක
    message_text = (
        f"🔥 *DORA WEB SITE* 🔥\n\n"
        f"✨ Welcome *{first_name}*!\n\n"
        f"📍 ඔබගේ *Live Location* එක බෙදාගැනීමට පහත බටන් එක ඔබන්න.\n"
        f"⚡ Location එක Allow කළාම automatic ලෙස අපට ලැබෙනවා.\n\n"
        f"🔒 *Secure & Encrypted* | 🔴 *Dora Security*"
    )
    
    # Web App Button එක (Auto link එක)
    keyboard = [[
        InlineKeyboardButton(
            text="📍 OPEN LIVE LOCATION", 
            web_app=WebAppInfo(url=unique_link)
        )
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        message_text,
        parse_mode="Markdown",
        reply_markup=reply_markup
    )
    logger.info(f"User {user_id} started bot - Link generated")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "🤖 *DORA Bot Help*\n\n"
        "/start - Generate your location link\n"
        "/help - Show this message\n\n"
        "⚡ How it works:\n"
        "1. Click OPEN LIVE LOCATION\n"
        "2. Click ALLOW on the webpage\n"
        "3. Your location is sent to us securely"
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    
    logger.info("🤖 DORA Bot is running...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
