from aiogram.fsm.state import StatesGroup, State


class BackStates(StatesGroup):
    main_page = State()
    del_status = State()
    location = State()
    nearest_branch = State()
    category_ = State()
    product_ = State()
    quantity = State()


class BranchesStates(StatesGroup):
    main = State()
    location = State()


class RegisterStates(StatesGroup):
    name = State()
    phone = State()
    change_phone = State()

