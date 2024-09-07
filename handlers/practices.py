from aiogram import Router, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import json
import os

router = Router()

# Определяем абсолютный путь к файлам
current_dir = os.path.dirname(__file__)  # Директория текущего файла
practices_path = os.path.join(current_dir, '..', 'data', 'practices.json')

# Загрузка описания практик
with open(practices_path, 'r', encoding='utf-8') as f:
    practices = json.load(f)["practices"]

# Обработчик для возврата к списку практик
@router.callback_query(lambda c: c.data == "back_to_practices")
async def back_to_practices_handler(callback_query: types.CallbackQuery):
    # Возвращаем пользователя к списку всех практик
    buttons = [
        [InlineKeyboardButton(text=practice["title"], callback_data=practice_key)]
        for practice_key, practice in practices.items()
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    await callback_query.message.answer("Выберите практику:", reply_markup=keyboard)
    await callback_query.answer()

# Обработчик для выбора практики (аннотация + список техник)
@router.callback_query(lambda c: c.data in practices)
async def practice_callback_handler(callback_query: types.CallbackQuery):
    practice_key = callback_query.data
    practice = practices.get(practice_key)

    if not practice:
        await callback_query.message.answer("Практика не найдена.")
        return

    # Отправка аннотации с Markdown
    annotation = practice["annotation"]
    content = practice.get("content", {})
    photo_url = content.get("photo_url")
    video_url = content.get("video_url")

    if photo_url:
        await callback_query.message.answer_photo(photo_url, caption=annotation, parse_mode="Markdown")
    elif video_url:
        await callback_query.message.answer_video(video_url, caption=annotation, parse_mode="Markdown")
    else:
        await callback_query.message.answer(annotation, parse_mode="Markdown")

    # Отображение списка техник
    techniques = practice.get("techniques", {})
    if not techniques:
        await callback_query.message.answer("Техники не найдены.")
        return

    # Формирование кнопок для каждой техники с использованием '::' в callback_data
    buttons = [
        [InlineKeyboardButton(text=technique["title"], callback_data=f"{practice_key}::{technique_key}")]
        for technique_key, technique in techniques.items()
    ]

    # Добавляем кнопку "Вернуться назад"
    buttons.append([InlineKeyboardButton(text="Вернуться назад", callback_data="back_to_practices")])
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    await callback_query.message.answer("Выберите технику:", reply_markup=keyboard)
    await callback_query.answer()

# Обработчик для выбора техники (контент техники)
@router.callback_query(lambda c: "::" in c.data)
async def technique_callback_handler(callback_query: types.CallbackQuery):
    try:
        # Разделяем строку по '::'
        practice_key, technique_key = callback_query.data.split("::", 1)
    except ValueError:
        await callback_query.message.answer("Некорректный формат данных.")
        await callback_query.answer()
        return

    # Получаем практику и технику
    practice = practices.get(practice_key, {})
    technique = practice.get("techniques", {}).get(technique_key)

    if not technique:
        await callback_query.message.answer("Техника не найдена.")
        await callback_query.answer()
        return

    content = technique["content"]
    text = content.get("text", "")

    # Отправка текста техники с Markdown
    await callback_query.message.answer(text, parse_mode="Markdown")

    # Кнопка для возврата к списку техник
    buttons = [[InlineKeyboardButton(text="Вернуться назад", callback_data=practice_key)]]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    await callback_query.message.answer("Выберите действие:", reply_markup=keyboard)
    await callback_query.answer()





