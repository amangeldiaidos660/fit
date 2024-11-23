import json
import logging
import os
from telebot.types import Message
from keyboards import main_keyboard
from progress import show_progress_menu
from auth import auth_bot
from recognition import analyze_text
# from config import TEMP_FOLDER
# from voice_to_text import transcribe_audio
from pydub import AudioSegment
import tempfile
import whisper


FFMPEG_PATH = r"C:\Users\amang\Desktop\fit\bot\ffmpeg\bin\ffmpeg.exe"
FFPROBE_PATH = r"C:\Users\amang\Desktop\fit\bot\ffmpeg\bin\ffprobe.exe"

os.environ["FFMPEG_BINARY"] = FFMPEG_PATH
os.environ["FFPROBE_BINARY"] = FFPROBE_PATH
os.environ["PATH"] += os.pathsep + r"C:\Users\amang\Desktop\fit\bot\ffmpeg\bin"

AudioSegment.ffmpeg = FFMPEG_PATH
AudioSegment.ffprobe = FFPROBE_PATH

model = whisper.load_model("base")  

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def start(bot, message: Message):
    bot.send_message(
        message.chat.id,
        "Добро пожаловать! Выберите команду из меню или отправьте голосовое сообщение.",
        reply_markup=main_keyboard,
    )

def handle_menu_command(bot, message: Message):
    if message.text == "Войти":
        bot.reply_to(message, "Вы вошли в систему. Что вы хотите сделать дальше?")
        auth_bot(bot, message.chat.id)
    elif message.text == "Записать тренировку":
        bot.reply_to(message, "Пожалуйста, выберите тип тренировки и введите данные.")
    elif message.text == "Мой прогресс":
        show_progress_menu(bot, message.chat.id)
    else:
        bot.reply_to(message, "Пожалуйста, используйте меню для выбора команд.")


def handle_voice_message(bot, message):
    try:
        file_info = bot.get_file(message.voice.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".ogg") as temp_ogg:
            temp_ogg.write(downloaded_file)
            ogg_path = temp_ogg.name

        wav_path = ogg_path.replace(".ogg", ".wav")
        audio = AudioSegment.from_file(ogg_path)
        audio.export(wav_path, format="wav")

        result = model.transcribe(wav_path)
        text = result.get("text", "").strip()

        os.remove(ogg_path)
        os.remove(wav_path)

        if text:
            analysis_result = analyze_text(text)
            parsed_result = json.loads(analysis_result)

            response = "Распознанный текст:\n"
            for item in parsed_result:
                if "exercise" in item:
                    exercise = item["exercise"]
                    count = item.get("count")
                    if count:
                        response += f"{exercise.capitalize()}: {count} раз\n"
                    else:
                        response += f"{exercise.capitalize()}: количество не указано\n"
                elif "message" in item:
                    response += item["message"]

            bot.send_message(message.chat.id, response)
        else:
            bot.send_message(message.chat.id, "К сожалению, не удалось распознать текст.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: {e}")

