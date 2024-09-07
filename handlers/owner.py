from aiogram import Router, types
from aiogram.exceptions import TelegramAPIError  # Используем корректное исключение
import json
import os
from config import bot  # Не забудь импортировать объект bot

router = Router()

# Определяем путь к файлу users.json
current_dir = os.path.dirname(__file__)
users_file_path = os.path.join(current_dir, '..', 'data', 'users.json')

# ID владельца бота (замени на свой chat_id)
BOT_OWNER_ID = 530456247  # Заменить на свой chat_id

# Функция для рассылки сообщения всем пользователям
async def broadcast_message(text):
    with open(users_file_path, 'r', encoding='utf-8') as f:
        users = json.load(f)

    for chat_id in users:
        try:
            await bot.send_message(chat_id, text)
        except TelegramAPIError as e:
            print(f"Не удалось отправить сообщение пользователю {chat_id}: {e}")

# Обработчик для сообщений от владельца бота
@router.message()
async def handle_owner_message(message: types.Message):
    if message.from_user.id == BOT_OWNER_ID:
        # Если сообщение от владельца, делаем рассылку
        await broadcast_message(message.text)
        await message.answer("Сообщение разослано всем пользователям.")
    else:
        # Если сообщение не от владельца, просто отвечаем, что это частный бот
        await message.answer("Вы не авторизованы для отправки сообщений другим пользователям.")

