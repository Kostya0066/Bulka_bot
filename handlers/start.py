from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import json
import os

router = Router()

# Определяем абсолютный путь к файлам welcome_message.json, practices.json и users.json
current_dir = os.path.dirname(__file__)  # Директория текущего файла
welcome_message_path = os.path.join(current_dir, '..', 'data', 'welcome_message.json')
practices_path = os.path.join(current_dir, '..', 'data', 'practices.json')
users_file_path = os.path.join(current_dir, '..', 'data', 'users.json')  # Файл для хранения пользователей

# Загрузка JSON файлов
with open(welcome_message_path, 'r', encoding='utf-8') as f:
    welcome_message = json.load(f)["welcome_message"]

with open(practices_path, 'r', encoding='utf-8') as f:
    practices = json.load(f)["practices"]

# Функция для сохранения chat_id пользователя
def save_user(chat_id):
    # Проверяем, существует ли файл users.json
    if os.path.exists(users_file_path):
        with open(users_file_path, 'r', encoding='utf-8') as f:
            users = json.load(f)
    else:
        users = []

    # Добавляем chat_id, если его ещё нет в списке
    if chat_id not in users:
        users.append(chat_id)
        with open(users_file_path, 'w', encoding='utf-8') as f:
            json.dump(users, f)

@router.message(Command("start"))  # Используем фильтр команд
async def send_welcome(message: types.Message):
    # Сохраняем chat_id пользователя
    chat_id = message.chat.id
    save_user(chat_id)

    text = welcome_message['text']
    photo_url = welcome_message['photo_url']
    video_url = welcome_message['video_url']

    # Отправка приветственного сообщения
    if photo_url:
        await message.answer_photo(photo_url, caption=text)
    elif video_url:
        await message.answer_video(video_url, caption=text)
    else:
        await message.answer(text)

    # Создание Inline-кнопок для выбора практики
    buttons = [
        [InlineKeyboardButton(text=practice["title"], callback_data=practice_key)]
        for practice_key, practice in practices.items()
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    await message.answer("Выберите практику:", reply_markup=keyboard)







