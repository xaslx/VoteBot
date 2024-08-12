import asyncio
from logger import logger

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.redis import Redis, RedisStorage

from app.db_service import start_db
from app.handlers import router
from app.keyboards import set_main_menu
from config import settings
from database import connection
import sentry_sdk
from sqlite3 import OperationalError
from aiogram.client.session.aiohttp import AiohttpSession


sentry_sdk.init(
    dsn=settings.dsn,
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)





async def start_bot():
    try:
        await start_db()
    except OperationalError:
        logger.error('Ошибка создания таблиц в базе данных, при запуске бота.')
        raise OperationalError('Не удалось создать таблицы')
    logger.info('Бот запущен')


async def stop_bot():
    connection.close()
    logger.info('Бот выключен')


async def main():
    session: AiohttpSession = AiohttpSession(proxy='http://proxy.server:3128') #для деплоя pythonanywhere
    bot: Bot = Bot(
        token=settings.TOKEN_BOT, 
        default=DefaultBotProperties(parse_mode="HTML"),
        session=session
    )
    redis: Redis = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
    storage: RedisStorage = RedisStorage(redis=redis)
    await bot.delete_webhook(True)
    dp: Dispatcher = Dispatcher(storage=storage)
    dp.include_router(router)
    dp.startup.register(start_bot)
    dp.startup.register(set_main_menu)
    dp.shutdown.register(stop_bot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info('Остановка бота')
