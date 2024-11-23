import json
import logging
import os
from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton
from keyboards import get_main_keyboard
from auth import auth_bot
from recognition import analyze_text
from save import save_training_data
from config import user_status
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

temp_data = {}


def start(bot, message: Message):
    chat_id = message.chat.id
    is_authenticated = user_status.get(chat_id, False)

    if is_authenticated:
        bot.send_message(
            chat_id,
            "Добро пожаловать! Выберите команду из меню или отправьте голосовое сообщение.",
            reply_markup=get_main_keyboard(authenticated=True)
        )
    else:
        bot.send_message(
            chat_id,
            "Для доступа войдите в систему.",
            reply_markup=get_main_keyboard(authenticated=False)
        )


def handle_menu_command(bot, message: Message):
    chat_id = message.chat.id
    is_authenticated = user_status.get(chat_id, False)

    if message.text == "Войти":
        if not is_authenticated:
            auth_bot(bot, chat_id)
        else:
            bot.reply_to(
                message,
                "Вы уже вошли в систему.",
                reply_markup=get_main_keyboard(authenticated=True)
            )
    elif message.text == "Выйти":
        if is_authenticated:
            user_status[chat_id] = False
            bot.reply_to(
                message,
                "Вы успешно вышли из системы.",
                reply_markup=get_main_keyboard(authenticated=False)
            )
        else:
            bot.reply_to(
                message,
                "Вы уже не в системе.",
                reply_markup=get_main_keyboard(authenticated=False)
            )
    else:
        bot.reply_to(
            message,
            "Пожалуйста, используйте меню для выбора команд.",
            reply_markup=get_main_keyboard(authenticated=is_authenticated)
        )




def handle_voice_message(bot, message):
    chat_id = message.chat.id
    is_authenticated = user_status.get(chat_id, False)

    if not is_authenticated:
        bot.send_message(chat_id, "Для отправки голосового сообщения войдите в систему.")
        return

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
            process_text(bot, chat_id, text)
        else:
            bot.send_message(chat_id, "К сожалению, не удалось распознать текст.")
    except Exception as e:
        bot.send_message(chat_id, f"Произошла ошибка: {e}")


def handle_text_message(bot, message):
    chat_id = message.chat.id
    is_authenticated = user_status.get(chat_id, False)

    if not is_authenticated:
        bot.send_message(chat_id, "Для отправки текстового сообщения войдите в систему.")
        return

    text = message.text.strip()
    if text:
        try:
            process_text(bot, chat_id, text)
        except Exception as e:
            bot.send_message(chat_id, f"Произошла ошибка при обработке текста: {e}")
    else:
        bot.send_message(chat_id, "Сообщение пустое. Пожалуйста, отправьте текст для анализа.")


def process_text(bot, chat_id, text):
    try:
        analysis_result = analyze_text(text)
        parsed_result = json.loads(analysis_result)

        temp_data[chat_id] = parsed_result

        response = "Распознанный текст:\n"
        has_exercises = False

        for item in parsed_result:
            if "exercise" in item:
                exercise = item["exercise"]
                count = item.get("count")
                has_exercises = True
                if count:
                    response += f"{exercise.capitalize()}: {count} раз\n"
                else:
                    response += f"{exercise.capitalize()}: количество не указано\n"
            elif "message" in item:
                response += item["message"]

        bot.send_message(chat_id, response)

        if has_exercises:
            markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add(KeyboardButton("Сохранить"), KeyboardButton("Отмена"))
            bot.send_message(chat_id, "Что вы хотите сделать с этой записью?", reply_markup=markup)
    except Exception as e:
        bot.send_message(chat_id, f"Произошла ошибка: {e}")


def handle_save_or_cancel(bot, message):
    chat_id = message.chat.id
    if message.text == "Сохранить":
        parsed_result = temp_data.get(chat_id)

        if parsed_result:
            save_training_data(chat_id, parsed_result)

            bot.send_message(
                chat_id,
                "Запись сохранена!",
                reply_markup=get_main_keyboard(authenticated=user_status.get(chat_id, False))
            )
        else:
            bot.send_message(
                chat_id,
                "Нет данных для сохранения. Попробуйте снова.",
                reply_markup=get_main_keyboard(authenticated=user_status.get(chat_id, False))
            )

    elif message.text == "Отмена":
        bot.send_message(
            chat_id,
            "Запись отменена.",
            reply_markup=get_main_keyboard(authenticated=user_status.get(chat_id, False))
        )

    temp_data.pop(chat_id, None)
