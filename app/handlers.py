from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup
from app.keyboards import public_or_anonym as kb_public_anonym
from app.keyboards import get_inline_kb
from config import settings
from aiogram.fsm.context import FSMContext
from config import settings
from app.schema import Poll, CancelPoll

router: Router = Router()



LIST_ADMINS: list[str] = settings.LIST_ADMINS



@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        f'Это бот который поможет вам создать опрос и отправить его на канал "Опросник"\n'
        f'<b>Чтобы создать опрос введи /create_poll</b>', parse_mode='HTML')


@router.message(Command('help'))
async def get_help(message: Message):
    await message.answer(
        f'<b>Доступные команды:</b>\n'
        f'/start - Запустить бота\n'
        f'/create_poll -Создать опрос\n'
        f'/help - все команды\n',
        parse_mode='HTML'
        )
    

@router.message(Command('create_poll'))
async def cmd_start(message: Message, state: FSMContext):
    await state.set_state(Poll.anonymous)
    await message.answer(f'Для начала выбери какой будет опрос. (Анонимный или Публичный)', reply_markup=kb_public_anonym)

@router.message(F.text.in_(('Анонимный', 'Публичный')), Poll.anonymous)
async def poll_anonymous(message: Message, state: FSMContext):
    await state.update_data(anonymous=message.text, user_id=message.from_user.id)
    await state.set_state(Poll.title)
    await message.answer('Теперь напиши вопрос для опроса')

@router.message(Poll.title)
async def poll_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(Poll.one_answer)
    await message.answer('Отправь первый ответ')


@router.message(Poll.one_answer)
async def poll_one_answer(message: Message, state: FSMContext):
    await state.update_data(one_answer=message.text)
    await state.set_state(Poll.two_answer)
    await message.answer('Отправь второй ответ')

@router.message(Poll.two_answer)
async def poll_two_question(message: Message, state: FSMContext):
    await state.update_data(two_answer=message.text)
    info: dict = await state.get_data()
    is_anonymous: bool = True if info['anonymous'] == 'Анонимный' else False
    inline_kb: InlineKeyboardMarkup = await get_inline_kb(user_id=message.from_user.id)

    for admin in LIST_ADMINS:
        await message.bot.send_poll(
            chat_id=admin, 
            question=info['title'],
            options=[
                info['one_answer'],
                info['two_answer']
            ],
            reply_markup=inline_kb,
            is_anonymous=is_anonymous
    )
    await message.answer('Ваш опрос отправлен на модерацию.')


@router.message()
async def echo(message: Message):
    await message.answer('Это неизвестная команда. Чтобы посмотреть все доступные команды введите /help')

@router.callback_query(F.data.startswith('cancel'))
async def cancel(callback: CallbackQuery, state: FSMContext):
    
    user_id: int = int(callback.data.split(":")[1])
    await callback.bot.send_message(chat_id=user_id, text="Ваш опрос был отклонен модератором.")
    await callback.answer("Опрос отклонен.")

@router.callback_query(F.data.startswith('accept'))
async def cancel(callback: CallbackQuery):
    await callback.answer()
    user_id: int = int(callback.data.split(":")[1])
    await callback.bot.send_message(chat_id=user_id, text="Ваш опрос был принят модерацией, и скоро появится на канале.")
