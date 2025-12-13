from app.config import settings
import telegram  # python-telegram-bot

bot = telegram.Bot(token=settings.TELEGRAM_BOT_TOKEN)

def post_to_telegram(content: str, image_url: str = None, schedule_time: str = None):
    # Упрощено, без scheduling
    if image_url:
        bot.send_photo(chat_id="@channel", photo=image_url, caption=content)
    else:
        bot.send_message(chat_id="@channel", text=content)
    return "Posted to Telegram"