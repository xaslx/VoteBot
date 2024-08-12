from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from aiogram import Bot
from config import settings

bot: Bot = Bot(settings.TOKEN_BOT)

async def get_inline_kb(id_db: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅", callback_data=f"accept:{id_db}"),
                InlineKeyboardButton(text="❌", callback_data=f"cancel:{id_db}"),
            ]
        ]
    )

async def set_main_menu(bot: Bot):

    main_menu_commands = [
        BotCommand(command='/start',
                   description='Запуск бота'),
        BotCommand(command='/create_poll',
                   description='Создать опрос'),
        BotCommand(command='/help',
                   description='Все команды'),
        BotCommand(command='/cancel',
                   description='Отменить создание опроса'),
    ]

    await bot.set_my_commands(main_menu_commands)