"""
Config package
"""
from os import getenv
from dotenv import load_dotenv

load_dotenv()

MAX_RETRY_ATTEMPTS = 2
DEFAULT_TIMEOUT = 30

REST_API_HOST = getenv('REST_API_HOST', '0.0.0.0')
REST_API_PORT = getenv('CLIENT_PORT', '8000')

CHAT_URL = f'http://{REST_API_HOST}:{REST_API_PORT}/chat'
BOT_TOKEN = getenv('BOT_TOKEN')