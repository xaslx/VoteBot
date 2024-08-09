from aiogram import Bot, Dispatcher
import asyncio
import logging
from config import settings
from app.handlers import router




async def main():

    bot: Bot = Bot(token=settings.TOKEN_BOT)
    dp: Dispatcher = Dispatcher()

    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
