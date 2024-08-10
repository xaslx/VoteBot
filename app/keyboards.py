from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton, 
                           InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButtonPollType)



async def get_inline_kb(user_id: int, title: str, one_answer: str, two_answer: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='✅', 
                    callback_data=f'accept:{user_id}:{title}:{one_answer}:{two_answer}'
                ),
                InlineKeyboardButton(
                    text='❌', 
                    callback_data=f'cancel:{user_id}'
                )
            ]
        ]
    )
