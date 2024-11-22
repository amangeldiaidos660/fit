import telebot
from config import BOT_TOKEN
from handlers import start, handle_menu_command, handle_voice_message
from progress import handle_progress_buttons

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=["start"])
def start_command(message):
    start(bot, message)

@bot.message_handler(content_types=["text"])
def text_command_handler(message):
    handle_menu_command(bot, message)

@bot.message_handler(content_types=["voice"])
def voice_command_handler(message):
    handle_voice_message(bot, message)

@bot.callback_query_handler(func=lambda call: call.data.startswith("progress"))
def progress_buttons_handler(call):
    handle_progress_buttons(bot, call)

if __name__ == "__main__":
    bot.infinity_polling()
