from aiogram import Bot
from .init_dispatcher import init_dispatcher
from config import BOT_TOKEN


async def run_bot() -> None:
    """
    Запуск бота
    """
    dispatcher = await init_dispatcher()
    # запуск бота
    bot = Bot(token=BOT_TOKEN)
    await dispatcher.start_polling(bot)