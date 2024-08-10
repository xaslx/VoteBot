from aiogram import Bot, Dispatcher
import asyncio
import logging
from config import settings
from app.handlers import router
from aiogram.fsm.storage.redis import RedisStorage, Redis



async def main():

    bot: Bot = Bot(token=settings.TOKEN_BOT)
    redis: Redis = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
    storage: RedisStorage = RedisStorage(redis=redis)

    dp: Dispatcher = Dispatcher(storage=storage)

    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
