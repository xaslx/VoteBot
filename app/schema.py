from aiogram.fsm.state import State, StatesGroup



class Poll(StatesGroup):
    title: State = State()
    answers: State = State()