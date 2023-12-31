"""Модуль для считывания .env"""

from envparse import Env

env = Env()
env.read_envfile(path="./.env")

DB_USER = env.str("DB_USER", default="postgres_test")
DB_PASS = env.str("DB_PASS", default="postgres_test")
DB_NAME = env.str("DB_NAME", default="postgres_test")
DB_HOST = env.str("DB_HOST", default="localhost")
REAL_DATABASE_URL = env.str(
    "REAL_DATABASE_URL",
    default=f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}"
)
REDIS_URL = env.str("REDIS_URL", default="127.0.0.1:6379")
TIME_EXPIRE = env.float("REDIS_TIME_EXPIRE")

BOT_TOKEN = env.str("BOT_TOKEN")
