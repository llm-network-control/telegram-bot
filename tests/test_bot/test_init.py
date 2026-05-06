"""
Test bot/__init__.py
"""
from unittest.mock import AsyncMock

import pytest

from bot import run_bot


@pytest.mark.asyncio
async def test_run_bot(mocker):
    """
    Test run_bot: success
    """

    mock_dispatcher = mocker.Mock()
    mock_dispatcher.start_polling = AsyncMock(return_value='started')

    mocker.patch(
        "bot.init_dispatcher.Dispatcher",
        return_value=mock_dispatcher
    )

    await run_bot()
    mock_dispatcher.start_polling.assert_called_once()
