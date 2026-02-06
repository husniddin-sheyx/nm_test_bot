from aiogram.fsm.state import State, StatesGroup

class ValidatedFileState(StatesGroup):
    waiting_for_action = State()  # File valid, waiting for Shuffle/Extract
