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


create_pool: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Создать опрос')]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder='Нажми на кнопку...'
)


inline_kb: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='✅', callback_data='accept'), InlineKeyboardButton(text='❌', callback_data='cancel')]
    ]
)
