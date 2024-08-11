from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def get_inline_kb(id_db: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='✅', 
                    callback_data=f'accept:{id_db}'
                ),
                InlineKeyboardButton(
                    text='❌', 
                    callback_data=f'cancel:{id_db}'
                )
            ]
        ]
    )
