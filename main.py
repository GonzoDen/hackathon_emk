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

SEND_PHOTOS, STATE2, STATE3, STATE4, STATE5, PRESENT_WORD, CHECK_WORD = range(7)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    reply_keyboard = [["Загрузить свои анализы"]]
    await update.message.reply_text(
        "Здравствуйте, <b>Адель Шакирова!</b> "
        "Я показываю анализ, оценку медицинских данных, "
        "также даю персонализированные советы и предотвращаю последствия.",
        parse_mode=telegram.constants.ParseMode.HTML,
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True,
                                         resize_keyboard=True
                                         ),
    )
    return SEND_PHOTOS


async def send_photos(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.message.from_user.id
    reply_keyboard = [["Да"]]

    photo_path_dec = 'Dec_2023.jpeg'
    photo_path_jan = 'Jan_2024.jpeg'

    try:
        # Check if the file exists
        with open(photo_path_dec, 'rb') as photo_file:
            # Send photo
            await context.bot.send_photo(chat_id=user_id, photo=InputFile(photo_file), caption='Ноябрь 2023')
    except Exception as e:
        print(f"Error sending photo: {e}")

    try:
        # Check if the file exists
        with open(photo_path_jan, 'rb') as photo_file:
            # Send photo
            await context.bot.send_photo(chat_id=user_id, photo=InputFile(photo_file), caption='Декабрь 2023')
    except Exception as e:
        print(f"Error sending photo: {e}")

    await update.message.reply_text(
        "Проанализируем?",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True,
                                         resize_keyboard=True
                                         ),
    )

    # context.bot.send_photo(chat_id=user_id, photo=InputFile('http://lnkiy.in/sample_image_1'), caption='Текст')

    return STATE2


async def state2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.message.from_user.id
    reply_keyboard = [["Оценить анализ"]]

    await update.message.reply_text(
        "Результаты Общего Анализа Крови за ноябрь 2023: \n\n"
        "Общий белок 71,8 г/л- НОРМА Мочевина 3,2 ммоль/л - НОРМА \n"
        "Креатинин 55,2 мкмоль/л- НОРМА \n"
        "Тимоловая проба 1,5 ед. - НОРМА \n"
        "Билирубин общий 6,1 мкмоль/л- НОРМА \n"
        "прямой 0,7 мкмоль/л - НОРМА \n"
        "АЛТ 13,1 ед/л - НИЖЕ НОРМЫ (норма у женщин — до 31 ед/л) \n"
        "АСТ 19,9 ед/л - НОРМА \n"
        "Глюкоза крови 5,13 ммоль/л - ВЫШЕ НОРМЫ (Норма глюкозы у женщин составляет 3,3-5,5 ммоль/л)",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True,
                                         resize_keyboard=True
                                         ),
    )

    await update.message.reply_text(
        "Результаты Общего Анализа Крови за декабрь 2023: \n\n"
        "Общий белок 66,3 г/л- НОРМА \n "
        "Креатинин 55,2 мкмоль/л- НОРМА \n"
        "Тимоловая проба 1,5 ед. - НОРМА \n"
        "Билирубин общий 6,1 мкмоль/л- НОРМА\n"
        "прямой 0,7 мкмоль/л - НОРМА\n"
        "АЛТ 33,5 ед/л - ВЫШЕ НОРМЫ (норма < 33 ед/л)\n"
        "АСТ 32,7 ед/л - ЧУТЬ ВЫШЕ НОРМЫ (норма до 32 Ед/л)\n"
        "Глюкоза крови 3,4 ммоль/л - НОРМА",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True,
                                         resize_keyboard=True
                                         ),
    )

    return STATE3


async def state3(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.message.from_user.id
    reply_keyboard = [["Покажи"]]

    photo_path = 'graph_2.png'

    try:
        # Check if the file exists
        with open(photo_path, 'rb') as photo_file:
            # Send photo
            await context.bot.send_photo(chat_id=user_id, photo=InputFile(photo_file),
                                         caption='Настоятельно советую обратиться к врачу-нефрологу, '
                                                 'у Вас резкоменяющийся АЛТ, нарушены работы почек и печени, '
                                                 'уровень мочевины, что  может быть проявлением инфекции мочеполовой '
                                                 'системы, опухоли, вследствие '
                                                 'чрезмерного употребления алкоголя и неправильного питания. '
                                                 'У Вас также нормализовался уровень сахара в крови, так держать!',
                                         reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True,
                                                                          resize_keyboard=True
                                                                          ),
                                         )
    except Exception as e:
        print(f"Error sending photo: {e}")

    await update.message.reply_text(
        "Показать, где именно проблема?",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True,
                                         resize_keyboard=True
                                         ),
    )

    return STATE4


async def state4(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.message.from_user.id
    reply_keyboard = [["Вау - этого ни один врач не увидел!"]]

    photo_path = 'ms_system.jpg'

    try:
        # Check if the file exists
        with open(photo_path, 'rb') as photo_file:
            # Send photo
            await context.bot.send_photo(chat_id=user_id, photo=InputFile(photo_file),
                                         caption='У вас все признаки инвазивной опухоли мочевого пузыря с признаками '
                                                 'инфильтрации в окружающие ткани, включая возможное поражение соседних '
                                                 'кровеносных сосудов.\n\n'
                                                 'При детальном анализе данных визуализации '
                                                 'обнаружена редкая и сложная патология, такая как фистула между '
                                                 'мочевым пузырём и прямой кишкой, что приводит к необычному общению '
                                                 ' между мочевыводящей и пищеварительной системами. \n\n'
                                                 'Это состояние вызвано вследствие травмы в 14 лет, рентген которого вы '
                                                 'загружали несколько лет назад.',
                                         reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True,
                                                                          resize_keyboard=True
                                                                          ),
                                         )
    except Exception as e:
        print(f"Error sending photo: {e}")

    return STATE5


async def state5(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Моя задача продлить вашу жизнь"
    )

    return ConversationHandler.END


def main() -> None:
    application = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            SEND_PHOTOS: [
                MessageHandler(filters.TEXT & ~(filters.COMMAND | filters.Regex("^Done$")), send_photos)],
            STATE2: [
                MessageHandler(filters.TEXT & ~(filters.COMMAND | filters.Regex("^Done$")), state2)],
            STATE3: [
                MessageHandler(filters.TEXT & ~(filters.COMMAND | filters.Regex("^Done$")), state3)],
            STATE4: [
                MessageHandler(filters.TEXT & ~(filters.COMMAND | filters.Regex("^Done$")), state4)],
            STATE5: [
                MessageHandler(filters.TEXT & ~(filters.COMMAND | filters.Regex("^Done$")), state5)],
        },
        fallbacks=[],
    )

    application.add_handler(conv_handler)

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
