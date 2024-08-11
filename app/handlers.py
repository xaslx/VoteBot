from aiogram import Bot, F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, Message

from app.bot_service import add_poll_in_db
from app.db_service import accept_poll, cancel_poll, find_poll
from app.schema import Poll
from config import settings

router: Router = Router()

bot: Bot = Bot(settings.TOKEN_BOT)


@router.message(CommandStart(), StateFilter(default_state))
async def cmd_start(message: Message):
    await message.answer(
        f'Это бот который поможет вам создать опрос и отправить его на канал "Опросник"\n'
        f"<b>Чтобы создать опрос - введите команду:</b>\n/create_poll"
    )


@router.message(Command(commands="cancel"), StateFilter(default_state))
async def process_cancel_command(message: Message):
    await message.answer(
        text="Отменять нечего. Вы пока не создаете опрос\n\n"
        "Чтобы перейти к созданию опроса - "
        "отправьте команду /create_poll"
    )


@router.message(Command(commands="cancel"), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(
        text="Вы отменили создание опроса\n\n"
        "Чтобы снова перейти к созданию опроса - "
        "отправьте команду /create_poll"
    )
    await state.clear()


@router.message(Command("help"), StateFilter(default_state))
async def help_cmd(message: Message):
    await message.answer(
        text="<b>Доступные команды:</b>\n\n"
        "/start   -   Запустить бота\n"
        "/create_poll   -   Создать опрос\n"
        "/help   -   Все команды\n"
        "/cancel   -   Отменить создание опроса"
    )


@router.message(Command("create_poll"), StateFilter(default_state))
async def cmd_start(message: Message, state: FSMContext):
    await state.set_state(Poll.title)
    await message.answer(
        f"<b>Напишите вопрос для опроса</b>\n\nЕсли хотите отменить создание опроса - введите /cancel"
    )


@router.message(StateFilter(Poll.title), F.text)
async def poll_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.update_data(answers=[])
    await message.answer(
        "<b>Отправьте первый ответ</b>\n\nЧтобы завершить ввод ответов, отправьте команду /done.\nЕсли хотите отменить создание опроса - введите /cancel"
    )
    await state.set_state(Poll.answers)


@router.message(StateFilter(Poll.title), ~F.text)
async def poll_title_warning(message: Message):
    await message.answer(
        "Вопрос должен состоять только из текста.\nЕсли хотите отменить создание опроса - введите /cancel"
    )


@router.message(Command("done"), StateFilter(Poll.answers))
async def done_command(message: Message, state: FSMContext):
    data: dict[str, str | list[str]] = await state.get_data()
    answers: list[str] = data.get("answers", [])

    if len(answers) < 2:
        await message.answer("Вы должны добавить как минимум 2 варианта ответа.")
    else:
        await add_poll_in_db(message, state, data, answers)
        await state.clear()


@router.message(StateFilter(Poll.answers), F.text)
async def poll_answers(message: Message, state: FSMContext):
    data: dict[str, str | list[str]] = await state.get_data()
    answers: list[str] = data.get("answers", [])

    if message.text.lower() == "/done":
        await done_command(message, state)
        return

    if len(answers) >= 10:
        await message.answer(
            "<b>Вы достигли максимального количества вариантов ответа (10).</b>\n Завершите ввод командой /done."
        )
        return

    answers.append(message.text)
    await state.update_data(answers=answers)
    await message.answer(
        f"Вариант ответа добавлен. Всего добавлено {len(answers)} ответов.\n\n"
        f"Отправьте следующий ответ или команду /done для завершения.\n"
        f"Если хотите отменить создание опроса - введите /cancel"
    )


@router.callback_query(F.data.startswith("cancel"))
async def cancel(callback: CallbackQuery, state: FSMContext):
    id_in_db: int = int(callback.data.split(":")[1])
    poll: dict[str, str | list[str]] = await find_poll(poll_id=id_in_db)

    if poll["canceled"] == 0:
        username: str = (
            callback.from_user.username
            if callback.from_user.username
            else callback.from_user.first_name
        )
        await callback.message.delete_reply_markup()
        await callback.bot.send_message(
            chat_id=poll["user_id"], text="<b>Ваш опрос был отклонен модератором.</b>"
        )
        await callback.answer("Опрос отклонен.")
        await callback.message.answer(f"Администратор {username} , отклонил опрос ❌")
        await cancel_poll(poll_id=id_in_db)
    else:
        await callback.answer("Опрос уже был отклонен одним из администраторов")


@router.callback_query(F.data.startswith("accept"))
async def accept(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete_reply_markup()
    id_in_db: int = int(callback.data.split(":")[1])
    poll: dict[str, str | list[str]] = await find_poll(poll_id=id_in_db)

    if poll["accepted"] == 0:
        username: str = (
            callback.from_user.username
            if callback.from_user.username
            else callback.from_user.first_name
        )
        await callback.bot.send_message(
            chat_id=poll["user_id"],
            text="<b>Ваш опрос был принят модерацией, и скоро появится на канале.</b>",
        )
        await callback.message.answer(
            f"Администратор {username} , проверил и одобрил опрос ✅"
        )

        await callback.bot.send_poll(
            chat_id=settings.CHANNEL_ID,
            question=poll["title"],
            options=poll["answers"],
        )

        await accept_poll(poll_id=id_in_db)
    else:
        await callback.answer("Опрос уже был принят одним из администраторов")


@router.message(StateFilter(default_state))
async def echo(message: Message):
    await message.answer(
        "Это неизвестная команда. Чтобы посмотреть все доступные команды введите /help"
    )
