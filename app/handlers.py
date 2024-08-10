from aiogram import F, Router, Bot
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup
from app.keyboards import get_inline_kb
from config import settings
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from config import settings
from app.schema import Poll, CancelPoll



router: Router = Router()



LIST_ADMINS: list[str] = settings.LIST_ADMINS
bot: Bot = Bot(settings.TOKEN_BOT)


@router.message(CommandStart(), StateFilter(default_state))
async def cmd_start(message: Message):
    await message.answer(
        f'Это бот который поможет вам создать опрос и отправить его на канал "Опросник"\n'
        f'<b>Чтобы создать опрос введи /create_poll</b>', parse_mode='HTML')

@router.message(Command(commands='cancel'), StateFilter(default_state))
async def process_cancel_command(message: Message):
    await message.answer(
        text='Отменять нечего. Вы вне машины состояний\n\n'
             'Чтобы перейти к созданию опроса - '
             'отправьте команду /create_poll'
    )

@router.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(
        text='Вы вышли из машины состояний\n\n'
             'Чтобы снова перейти к созданию опроса - '
             'отправьте команду /create_poll'
    )
    await state.clear()


@router.message(Command('help'), StateFilter(default_state))
async def get_help(message: Message):
    await message.answer(
        f'<b>Доступные команды:</b>\n'
        f'/start - Запустить бота\n'
        f'/create_poll -Создать опрос\n'
        f'/help - все команды\n',
        parse_mode='HTML'
        )
    

@router.message(Command('create_poll'), StateFilter(default_state))
async def cmd_start(message: Message, state: FSMContext):
    await state.set_state(Poll.title)
    await message.answer(f'Напишите вопрос для опроса')

@router.message(StateFilter(Poll.title), F.text)
async def poll_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await message.answer('Отправь 1 ответ')
    await state.set_state(Poll.one_answer)

@router.message(StateFilter(Poll.title), ~F.text)
async def poll_title_warning(message: Message):
    await message.answer('Вопрос должен состоять только из текста.\nЕсли хотите отменить создание опроса - введите /cancel')

@router.message(StateFilter(Poll.one_answer), F.text)
async def poll_one_answer(message: Message, state: FSMContext):
    await state.update_data(one_answer=message.text)
    await message.answer('Отправь 2 ответ')
    await state.set_state(Poll.two_answer)

@router.message(StateFilter(Poll.one_answer), ~F.text)
async def poll_one_answer_warning(message: Message):
    await message.answer('Ответ должен состоять только из текста.\nЕсли хотите отменить создание опроса - введите /cancel')


@router.message(StateFilter(Poll.two_answer), F.text)
async def poll_two_answer(message: Message, state: FSMContext):
    await state.update_data(two_answer=message.text)
    info: dict = await state.get_data()
    inline_kb: InlineKeyboardMarkup = await get_inline_kb(
        user_id=message.from_user.id, 
        title=info['title'], 
        one_answer=info['one_answer'], 
        two_answer=message.text,
    )
    
    for admin in LIST_ADMINS:
        await message.bot.send_poll(
            chat_id=admin, 
            question=info['title'],
            options=[
                info['one_answer'],
                info['two_answer']
            ],
            reply_markup=inline_kb,
    )
    await message.answer('Ваш опрос отправлен на модерацию.')
    await state.clear()

@router.message(StateFilter(Poll.two_answer), ~F.text)
async def poll_two_answer_warning(message: Message):
    await message.answer('Ваш опрос отправлен на модерацию.')


@router.callback_query(F.data.startswith('cancel'))
async def cancel(callback: CallbackQuery, state: FSMContext):
    user_id: int = int(callback.data.split(":")[1])
    await callback.bot.send_message(chat_id=user_id, text="Ваш опрос был отклонен модератором.")
    await callback.answer("Опрос отклонен.")


@router.callback_query(F.data.startswith('accept'))
async def cancel(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = callback.data.split(":")
    user_id = int(data[1])
    title = data[2]
    one_answer = data[3]
    two_answer = data[4]

    
    await callback.bot.send_message(chat_id=user_id, text="Ваш опрос был принят модерацией, и скоро появится на канале.")
    await callback.bot.send_poll(
        chat_id=settings.CHANNEL_ID, 
        question=title,
        options=[one_answer, two_answer],
    )
    for admin in LIST_ADMINS:
        await bot.delete_message(callback.from_user.id. callback.message.id)
    

@router.message(StateFilter(default_state))
async def echo(message: Message):
    await message.answer('Это неизвестная команда. Чтобы посмотреть все доступные команды введите /help')