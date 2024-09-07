from aiogram import Dispatcher
from config import bot  # Используем объект bot из config.py

# Инициализация диспетчера
dp = Dispatcher()

# Функция для регистрации всех обработчиков
def register_all_handlers():
    from handlers import start, practices, navigation, owner  # Добавляем owner

    dp.include_router(start.router)
    dp.include_router(practices.router)
    dp.include_router(navigation.router)
    dp.include_router(owner.router)  # Подключаем обработчик owner

# Регистрация всех обработчиков
register_all_handlers()

