from email import message
from aiogram import F, Router, Bot
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup
from app.keyboards import get_inline_kb
from config import settings
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from config import settings
from app.schema import Poll



router: Router = Router()

bot: Bot = Bot(settings.TOKEN_BOT)

@router.message(CommandStart(), StateFilter(default_state))
async def cmd_start(message: Message):
    await message.answer(
        f'Это бот который поможет вам создать опрос и отправить его на канал "Опросник"\n'
        f'<b>Чтобы создать опрос - введите команду\n /create_poll</b>')

@router.message(Command(commands='cancel'), StateFilter(default_state))
async def process_cancel_command(message: Message):
    await message.answer(
        text='Отменять нечего. Вы пока не создаете опрос\n\n'
             'Чтобы перейти к созданию опроса - '
             'отправьте команду /create_poll'
    )

@router.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(
        text='Вы отменили создание опроса\n\n'
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
        f'/help - Все команды\n',
        f'/cancel - Отменить создание опроса'
        )
    

@router.message(Command('create_poll'), StateFilter(default_state))
async def cmd_start(message: Message, state: FSMContext):
    await state.set_state(Poll.title)
    await message.answer(f'<b>Напишите вопрос для опроса</b>\nЕсли хотите отменить создание опроса - введите /cancel')

@router.message(StateFilter(Poll.title), F.text)
async def poll_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await message.answer('<b>Отправьте 1 ответ</b>\nЕсли хотите отменить создание опроса - введите /cancel')
    await state.set_state(Poll.one_answer)

@router.message(StateFilter(Poll.title), ~F.text)
async def poll_title_warning(message: Message):
    await message.answer('Вопрос должен состоять только из текста.\nЕсли хотите отменить создание опроса - введите /cancel')

@router.message(StateFilter(Poll.one_answer), F.text)
async def poll_one_answer(message: Message, state: FSMContext):
    await state.update_data(one_answer=message.text)
    await message.answer('Отправьте 2 ответ\nЕсли хотите отменить создание опроса - введите /cancel')
    await state.set_state(Poll.two_answer)

@router.message(StateFilter(Poll.one_answer), ~F.text)
async def poll_one_answer_warning(message: Message):
    await message.answer('Ответ должен состоять только из текста.\nЕсли хотите отменить создание опроса - введите /cancel')


@router.message(StateFilter(Poll.two_answer), F.text)
async def poll_two_answer(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(two_answer=message.text)

    info: dict = await state.get_data()
    inline_kb: InlineKeyboardMarkup = await get_inline_kb(
        user_id=message.from_user.id, 
        title=info['title'], 
        one_answer=info['one_answer'], 
        two_answer=message.text,
    )
    
    #for admin
    await message.bot.send_message(chat_id=settings.ID_ADMINS_GROUP, text=f'Пользователь @{message.from_user.username} отправил опрос на проверку.')
    await message.bot.send_poll(
            chat_id=settings.ID_ADMINS_GROUP, 
            question=info['title'],
            options=[
                info['one_answer'],
                info['two_answer']
            ],
            reply_markup=inline_kb
    )
    
    #for user
    await message.answer('Так выглядит ваш опрос:')
    await bot.send_poll(
            chat_id=message.from_user.id, 
            question=info['title'],
            options=[
                info['one_answer'],
                info['two_answer']
            ]
    )
    await message.answer('Опрос был отправлен на проверку, если пройдет - то будет отправлен на канал.')
    await state.clear()


@router.message(StateFilter(Poll.two_answer), ~F.text)
async def poll_two_answer_warning(message: Message):
    await message.answer('Ответ должен состоять только из текста.\nЕсли хотите отменить создание опроса - введите /cancel')


@router.callback_query(F.data.startswith('cancel'))
async def cancel(callback: CallbackQuery, state: FSMContext):
    user_id: int = int(callback.data.split(":")[1])
    await callback.message.delete_reply_markup()
    await callback.bot.send_message(chat_id=user_id, text="Ваш опрос был отклонен модератором.")
    await callback.answer("Опрос отклонен.")
    await callback.message.answer(f'Администратор @{callback.from_user.username} , отклонил опрос ❌')


@router.callback_query(F.data.startswith('accept'))
async def cancel(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete_reply_markup()
    data: list[str] = callback.data.split(":")
    user_id: int = int(data[1])
    title: str = data[2]
    one_answer: str = data[3]
    two_answer: str = data[4]

    
    await callback.bot.send_message(chat_id=user_id, text="Ваш опрос был принят модерацией, и скоро появится на канале.")
    await callback.message.answer(f'Администратор @{callback.from_user.username} , проверил и одобрил опрос ✅')
    await callback.bot.send_poll(
        chat_id=settings.CHANNEL_ID, 
        question=title,
        options=[one_answer, two_answer],
    )

    

@router.message(StateFilter(default_state))
async def echo(message: Message):
    await message.answer('Это неизвестная команда. Чтобы посмотреть все доступные команды введите /help')