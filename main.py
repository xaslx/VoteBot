import os
from aiogram import F, Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
import asyncio
import logging
from config import settings


TOKEN_BOT: str = settings.TOKEN_BOT



bot: Bot = Bot(token=TOKEN_BOT)
dp: Dispatcher = Dispatcher()




async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
