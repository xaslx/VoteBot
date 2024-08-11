from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
import asyncio
import logging
from config import settings
from app.handlers import router
from aiogram.fsm.storage.redis import RedisStorage, Redis
from database import connection
from app.db_service import start_db



async def start_bot():
    await start_db()

async def stop_bot():
    await connection.close()


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
