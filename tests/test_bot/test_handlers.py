"""
Tests bot/handlers
"""
import pytest
from bot import handlers
from .mocks import MockInfoMessage


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