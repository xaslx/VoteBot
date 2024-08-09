from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton, 
                           InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButtonPollType)



public_or_anonym: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Анонимный')],
        [KeyboardButton(text='Публичный')]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder='Нажми на кнопку...'
)

async def get_inline_kb(user_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='✅', callback_data=f'accept:{user_id}'),
                InlineKeyboardButton(text='❌', callback_data=f'cancel:{user_id}')
            ]
        ]
    )