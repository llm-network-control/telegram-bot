"""
Основные обработчики
"""

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from api_client.client import get_json_dict
from config import CHAT_URL


router = Router()


async def info_handler(message: Message) -> None:
    """
    Информация о боте для пользователя
    """
    text = ('Привет. Я бот для поиска бесплатного WiFi'
            'Скинь мне список WiFi сетей,'
            'а я попробую найти для них пароли')
    await message.answer(text)


@router.message(Command('start'))
async def command_start_handler(message: Message) -> None:
    """
    Обработчик команды /start
    """
    await info_handler(message)


@router.message(Command('help'))
async def command_help_handler(message: Message) -> None:
    """
    Обработчик команды /help
    """
    await info_handler(message)


@router.message(~F.text.startswith("/"), ~F.file)
async def chat_handler(message: Message) -> None:
    """
    Чат с пользователем
    :param message: сообщение пользователя
    :return: None
    """
    text = message.text
    if len(text) < 5:
        await message.answer("Слишком короткое сообщение, введите понятный текст")
        return
    thinking = await message.answer("Думаю...")
    success, answer, error = await get_json_dict(
        CHAT_URL,
        text,
    )
    if not success:
        answer = error
    await thinking.edit_text(answer)
