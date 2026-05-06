"""
Tests bot/handlers
"""
import pytest
from bot import handlers
from .mocks import (
    MockInfoMessage,
    MockTooShortAnswerMessage,
    PositiveMessage,
    mock_get_json_dict,
)


@pytest.mark.asyncio
async def test_command_start_handler():
    """
    Test command_start_handler: positive
    """
    message = MockInfoMessage()
    await handlers.command_start_handler(message)
    expected_text = ('Привет. Я бот для поиска бесплатного WiFi. '
            'Скинь мне список WiFi сетей, '
            'а я попробую найти для них пароли')
    assert expected_text == message.text


@pytest.mark.asyncio
async def test_command_help_handler():
    """
    Test command_help_handler: positive
    """
    message = MockInfoMessage()
    await handlers.command_help_handler(message)
    expected_text = ('Привет. Я бот для поиска бесплатного WiFi. '
            'Скинь мне список WiFi сетей, '
            'а я попробую найти для них пароли')
    assert expected_text == message.text


@pytest.mark.asyncio
async def test_chat_handler_too_short_answer():
    """
    Test chat_handler: too short answer
    """
    message = MockTooShortAnswerMessage()
    await handlers.chat_handler(message)
    expected_text = "Слишком короткое сообщение, введите понятный текст"
    assert expected_text == message.text


@pytest.mark.asyncio
async def test_chat_handler_positive(mocker):
    """
    Test chat_handler: got response
    """
    message = PositiveMessage()
    mocker.patch('bot.handlers.get_json_dict', mock_get_json_dict)
    await handlers.chat_handler(message)
    expected_text = 'Я тестовый ответ'
    assert expected_text == message.thinking.text
