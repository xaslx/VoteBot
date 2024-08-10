from aiogram.fsm.state import State, StatesGroup



class Poll(StatesGroup):
    title: State = State()
    one_answer: State = State()
    two_answer: State = State()
