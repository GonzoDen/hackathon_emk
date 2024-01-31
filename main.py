from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("API_KEY_TELEGRAM")

import telegram
import logging
from telegram import __version__ as TG_VER
import re

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, InputFile
import asyncio
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters, PicklePersistence,
    Updater, JobQueue, CallbackContext
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

STATE1, STATE2, STATE3, DAILY_CHECK, HOME, PRESENT_WORD, CHECK_WORD = range(7)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    reply_keyboard = [["кнопка1"]]
    await update.message.reply_html(
       "Здравствуйте, Айгерим Ибрагимова!",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True,
                                         resize_keyboard=True
                                         ),
    )
    return STATE1

async def state1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.message.from_user.id
    reply_keyboard = [["кнопка2"]]
    await update.message.reply_html(
        "Проанализируем?",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True,
                                         resize_keyboard=True
                                         ),
    )

    photo_path = 'sample_1.jpeg'

    try:
        # Check if the file exists
        with open(photo_path, 'rb') as photo_file:
            # Send photo
            await context.bot.send_photo(chat_id=user_id, photo=InputFile(photo_file), caption='Текст3')
    except Exception as e:
        print(f"Error sending photo: {e}")

    try:
        # Check if the file exists
        with open(photo_path, 'rb') as photo_file:
            # Send photo
            await context.bot.send_photo(chat_id=user_id, photo=InputFile(photo_file), caption='Текст4')
    except Exception as e:
        print(f"Error sending photo: {e}")


    #context.bot.send_photo(chat_id=user_id, photo=InputFile('http://lnkiy.in/sample_image_1'), caption='Текст')

    return STATE2

async def state2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.message.from_user.id
    reply_keyboard = [["Дать оценку?"]]
    await update.message.reply_html(
        "Текстовые данные анализа",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True,
                                         resize_keyboard=True
                                         ),
    )

    return STATE3

async def state3(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.message.from_user.id
    reply_keyboard = [["Вау - этого ни один врач не увидел"]]

    photo_path = 'sample_1.jpeg'

    try:
        # Check if the file exists
        with open(photo_path, 'rb') as photo_file:
            # Send photo
            await context.bot.send_photo(chat_id=user_id, photo=InputFile(photo_file), caption='Оценка текст',
                                         reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True,
                                                                          resize_keyboard=True
                                                                          ),
                                         )
    except Exception as e:
        print(f"Error sending photo: {e}")


    return ConversationHandler.END

def main() -> None:
    application = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            STATE1: [
                MessageHandler(filters.TEXT & ~(filters.COMMAND | filters.Regex("^Done$")), state1)],
            STATE2: [
                MessageHandler(filters.TEXT & ~(filters.COMMAND | filters.Regex("^Done$")), state2)],
            STATE3: [
                MessageHandler(filters.TEXT & ~(filters.COMMAND | filters.Regex("^Done$")), state3)],
        },
        fallbacks=[],
    )

    application.add_handler(conv_handler)

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()