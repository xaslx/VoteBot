from aiogram.fsm.state import State, StatesGroup



class Poll(StatesGroup):
    anonymous: State = State()
    title: State = State()
    one_answer: State = State()
    two_answer: State = State()
    
class CancelPoll(StatesGroup):
    description: State = State()