import asyncio
from bot import bot, dp  # Импортируем инициализированные bot и dp из bot.py


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())


