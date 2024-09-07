from aiogram import Router, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import json
import os

router = Router()

# Определяем абсолютный путь к файлу practices.json
current_dir = os.path.dirname(__file__)  # Директория текущего файла
practices_path = os.path.join(current_dir, '..', 'data', 'practices.json')

# Загрузка описания практик
with open(practices_path, 'r', encoding='utf-8') as f:
    practices = json.load(f)["practices"]

# Обработчик для выбора практики с префиксом 'get_'
@router.callback_query(lambda c: c.data.startswith("get_"))
async def get_practice_callback_handler(callback_query: types.CallbackQuery):
    practice_key = callback_query.data.replace("get_", "")
    practice = practices.get(practice_key)

    if not practice:
        await callback_query.message.answer("Практика не найдена.")
        return

    content = practice["content"]
    text = practice["annotation"]  # Используем аннотацию вместо 'text'
    photo_url = content.get("photo_url")
    video_url = content.get("video_url")

    # Отправка контента практики
    if photo_url:
        await callback_query.message.answer_photo(photo_url, caption=text)
    elif video_url:
        await callback_query.message.answer_video(video_url, caption=text)
    else:
        await callback_query.message.answer(text)

    await callback_query.answer()

# Обработчик для возврата к списку практик
@router.callback_query(lambda c: c.data == "back_to_practices_nav")
async def back_to_practices_callback_handler(callback_query: types.CallbackQuery):
    # Возвращение к выбору практики
    buttons = [
        [InlineKeyboardButton(text=practice["title"], callback_data=f"get_{practice_key}")]
        for practice_key, practice in practices.items()
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    await callback_query.message.answer("Выберите практику:", reply_markup=keyboard)
    await callback_query.answer()



