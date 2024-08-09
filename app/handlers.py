import os
from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from app.keyboards import create_pool as kb_create_pool
from app.keyboards import public_or_anonym as kb_public_anonym
from app.keyboards import inline_kb
from config import settings

router: Router = Router()



LIST_ADMINS: list[str] = settings.LIST_ADMINS


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f'Это бот который поможет вам создать опрос и отправить его на канал "Опросник"')


@router.message(Command('help'))
async def get_help(message: Message):
    await message.answer(
        f'Это бот для отправки вашего опроса в группу "Опросник"\n\n'
        f'<b>Доступные команды:</b>\n'
        f'/start - запустить бота\n'
        f'/create_poll - создать опрос\n'
        f'/help - все команды\n',
        parse_mode='HTML'
        )
    

@router.message()
async def echo(message: Message):
    await message.answer('Это неизвестная команда. Чтобы посмотреть все доступные команды введите /help')


