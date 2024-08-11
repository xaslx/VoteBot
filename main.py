import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.redis import Redis, RedisStorage

from app.db_service import start_db
from app.handlers import router
from config import settings
from database import connection


async def start_bot():
    await start_db()

async def stop_bot():
    connection.close()


async def main():

    bot: Bot = Bot(token=settings.TOKEN_BOT, default=DefaultBotProperties(parse_mode='HTML'))
    redis: Redis = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
    storage: RedisStorage = RedisStorage(redis=redis)
    await bot.delete_webhook(True)
    dp: Dispatcher = Dispatcher(storage=storage)
    dp.include_router(router)
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)
    await dp.start_polling(bot)



if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
