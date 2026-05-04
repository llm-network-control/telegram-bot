import asyncio
import httpx
from . import errors
from config import MAX_RETRY_ATTEMPTS, DEFAULT_TIMEOUT


async def is_not_found_status(status: int) -> bool:
    """
    Страница не найдена 404
    :param status: код статуса
    :return:
    """
    return status == 404


async def is_retry_status(status: int) -> bool:
    """
    Статус при котором нужно делать retry
    :param status: код статуса
    """
    return status in (408, 429, 500, 502, 503, 504)


async def get_json_dict(
        url: str,
        message: str,
        attempts: int = int(MAX_RETRY_ATTEMPTS),
        timeout: int = int(DEFAULT_TIMEOUT),
) -> tuple[bool, list | dict, str]:
    """
    :param url: адрес в api
    :param message: текст сообщения
    :param attempts: количество попыток переподключения
    :param timeout: время ожидания
    :return: [успех, словарь ответа, текст ошибки]
    """
    last_error: Exception | None = None
    attempts = attempts + 1

    async with httpx.AsyncClient(timeout=timeout) as client:
        for attempt in range(1, attempts + 1):
            try:
                data = {
                    'message': message
                }

                print('SENDING REQUEST ON', url)
                response = await client.post(url, json=data)
                print('RESPONSE')
                print(response)
                response.raise_for_status()
                payload = response.json()
                print(payload)
                if isinstance(payload, dict):
                    return True, payload, ''
                return False, {}, 'Неправильный ответ от API'
            except httpx.TimeoutException as err:
                last_error = errors.ApiClientTimeoutError(str(err))
            except httpx.HTTPStatusError as err:
                status = err.response.status_code

                if await is_not_found_status(status):
                    return False, {}, f'Endpoint {url} не найден на сервере'

                try:
                    message = err.response.text
                except Exception:
                    message = "No response body"
                if await is_retry_status(status) and attempt < attempts:
                    last_error = errors.ApiClientHttpError(status, message)
                else:
                    # raise ApiClientHttpError(status, message) from err
                    return False, {}, f'Ошибка API {message}'
            except httpx.RequestError as err:
                last_error = errors.ApiClientNetworkError(str(err))

            if attempt < attempts:
                await asyncio.sleep(timeout)

        if last_error is not None:
            try:
                raise last_error
            except Exception as e:
                return False, {}, str(e)
        return False, {}, 'Неизвестная ошибка API'