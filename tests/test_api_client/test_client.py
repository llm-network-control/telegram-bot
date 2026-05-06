"""
Tests api_client/client
"""
from unittest.mock import AsyncMock

import httpx
import pytest

from api_client.client import get_json_dict

positive_test_data = [
    ({"response": "ok"}, (True, {"response": "ok"}, '')),
    ([{"wrong": "answer list"}], (False, {}, 'Неправильный ответ от API')),
]

@pytest.mark.asyncio
@pytest.mark.parametrize(
    "server_response_dict,expected_result",
    positive_test_data,
)
async def test_get_json_dict_positive(
        mocker,
        server_response_dict: dict,
        expected_result: tuple[bool, dict, str],
):
    """
    Test get_json_dict: server answer, got json
    """
    # --- mock response ---
    mock_response = mocker.Mock()
    mock_response.json.return_value = server_response_dict
    mock_response.raise_for_status.return_value = None

    # --- mock client ---
    mock_client = mocker.Mock()
    mock_client.post = AsyncMock(return_value=mock_response)

    # --- mock context manager ---
    mock_async_client = mocker.Mock()
    mock_async_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_async_client.__aexit__ = AsyncMock(return_value=None)

    # --- patch ---
    mocker.patch(
        "api_client.client.httpx.AsyncClient",
        return_value=mock_async_client
    )

    success, payload, error = await get_json_dict(
        url="http://test/api",
        message="hello"
    )

    assert expected_result == (success, payload, error)


exception_test_data = [
    (httpx.TimeoutException("timeout"), (False, {}, 'timeout')),
    (httpx.RequestError('request error'), (False, {}, 'request error')),
]

@pytest.mark.asyncio
@pytest.mark.parametrize(
    "side_effect,expected_result",
    exception_test_data,
)
async def test_get_json_exception_not_response(
        mocker,
        side_effect,
        expected_result,
    ):
    """
    Test get_json_dict: Got exception, no server response
    """

    # --- mock client ---
    mock_client = mocker.Mock()
    mock_client.post = AsyncMock(
        side_effect=side_effect
    )

    # --- mock context manager ---
    mock_async_client = mocker.Mock()
    mock_async_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_async_client.__aexit__ = AsyncMock(return_value=None)

    # --- patch ---
    mocker.patch(
        "api_client.client.httpx.AsyncClient",
        return_value=mock_async_client
    )

    success, payload, error = await get_json_dict(
        url="http://test/api",
        message="hello",
        attempts=1,
        timeout=1,
    )
    assert expected_result == (success, payload, error)



exception_response_test_data = [
    (
        404,
        '404 Not found',
        (False, {}, 'Endpoint http://test/api не найден на сервере')
    ),
    (
        666,
        '666 Status',
        (False, {}, 'Ошибка API 666 Status')
    ),
    (
        429,
        '429 Too Many Requests',
        (False, {}, 'Ошибка API 429 Too Many Requests')
    ),
    (
        400,
        None,
        (False, {}, 'Ошибка API No response body')
    ),
]

@pytest.mark.asyncio
@pytest.mark.parametrize(
    "response_status_code,response_text,expected_result",
    exception_response_test_data,
)
async def test_get_json_dict_error_response(
    mocker,
    response_status_code,
    response_text,
    expected_result,
):
    """
    Test get_json_dict: Got error, got server response
    """

    # --- mock response ---
    mock_response = mocker.Mock()
    mock_response.status_code = response_status_code
    mock_response.text = response_text

    # --- mock client ---
    mock_client = mocker.Mock()
    mock_client.post = AsyncMock(
        side_effect=httpx.HTTPStatusError(
            response_text,
            request=None,
            response=mock_response
        )
    )

    # --- mock context manager ---
    mock_async_client = mocker.Mock()
    mock_async_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_async_client.__aexit__ = AsyncMock(return_value=None)

    # --- patch ---
    mocker.patch(
        "api_client.client.httpx.AsyncClient",
        return_value=mock_async_client
    )

    success, payload, error = await get_json_dict(
        url="http://test/api",
        message="hello",
        attempts=1,
        timeout=1,
    )
    assert expected_result == (success, payload, error)
