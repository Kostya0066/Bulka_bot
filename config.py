import os
from dotenv import load_dotenv
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

# Загружаем переменные окружения из файла .env
load_dotenv()

# Получаем токен из переменной окружения
TOKEN = os.getenv('BOT_TOKEN')

if not TOKEN:
    raise ValueError("Не удалось получить токен. Убедитесь, что BOT_TOKEN указан в .env файле.")

# Инициализируем бота с использованием DefaultBotProperties для parse_mode
bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML
    )
)