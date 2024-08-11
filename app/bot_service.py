from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, Message

from app.db_service import insert_poll
from app.keyboards import get_inline_kb
from config import settings


async def add_poll_in_db(
    message: Message, state: FSMContext, data: dict, answers: list[str]
):
    username: str = (
        message.from_user.username
        if message.from_user.username
        else message.from_user.first_name
    )

    id_in_db: int = await insert_poll(
        username, message.from_user.id, data["title"], answers, accepted=0, canceled=0
    )

    inline_kb: InlineKeyboardMarkup = await get_inline_kb(id_db=id_in_db)

    await message.bot.send_message(
        chat_id=settings.ID_ADMINS_GROUP,
        text=f"Пользователь {username} отправил опрос на проверку.",
    )

    # for admin
    await message.bot.send_poll(
        chat_id=settings.ID_ADMINS_GROUP,
        question=data["title"],
        options=answers,
        reply_markup=inline_kb,
    )

    # for user
    await message.answer("<b>Так выглядит ваш опрос:</b>")
    await message.bot.send_poll(
        chat_id=message.from_user.id, question=data["title"], options=answers
    )
    await message.answer(
        "<b>Опрос был отправлен на проверку, если пройдет - то будет отправлен на канал.</b>"
    )
