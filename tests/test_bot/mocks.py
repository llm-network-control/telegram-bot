# pylint: disable=attribute-defined-outside-init
"""
Mocks for tests
"""

class MockInfoMessage:
    """
    Mock: from aiogram.types import Message
    """

    async def answer(self, text: str):
        """
        Mock message.answer
        """
        self.text = text


class MockTooShortAnswerMessage:
    """
    Mock: from aiogram.types import Message
    """

    def __init__(self):
        self.text = '1234'

    async def answer(self, text: str):
        """
        Mock message.answer
        """
        self.text = text


class PositiveMessage:
    """
    Mock: from aiogram.types import Message
    """

    def __init__(self):
        self.text = 'Я тестовый текст'

    async def answer(self, _):
        """
        mock message.thinking
        """
        self.thinking = PositiveMessage()
        return self.thinking

    async def edit_text(self, text: str):
        """
        Mock message.edit_text
        """
        self.text = text


async def mock_get_json_dict(_, __):
    """
    Mock from api_client.client import get_json_dict
    """
    success = True
    answer = {
        'response': 'Я тестовый ответ'
    }
    error = ''
    return success, answer, error
