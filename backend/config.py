import os
from typing import Callable

BASE_DIR = f'{os.path.dirname(os.path.realpath(__file__))}/'

DEFAULT_CONFIG = {
    'HOST_URL': 'http://localhost:8000',
    'DEFAULT_USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) '
                          'Gecko/20100101 Firefox/116.0',
    'JWT_SECRET': '<secret>',
    'JWT_ALGORITHM': 'HS256',
    'JWT_EXPIRATION': '180',  # days
    'DOWNLOAD_TIMEOUT': 15,
    'CHUNK_SIZE': 1024 * 1024,
    'DATA_DIR': 'data',
    'REDIS_URI': 'redis://localhost:6379/0',
    'DB_URI': 'postgresql+asyncpg://user:secret@db:5432/data',
    'LOGGING_DEFINITIONS': f'{BASE_DIR}logging.yml',
    'THUMB_WIDTH': 290,
    'THUMB_HEIGHT': 435,
    'MD5_BUFFER_SIZE': 1024 * 1024      # 1KB
}


def get_config(name: str, default=None, wrapper: Callable = None):
    if not wrapper:
        wrapper = lambda x: x  # NOQA
    return wrapper(os.getenv(name, DEFAULT_CONFIG.get(name, default)))
