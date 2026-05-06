"""
Mocks for tests
"""

class MockInfoMessage:
    """
    Mock: from aiogram.types import Message
    """

    async def answer(self, text: str):
        self.text = text
