from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.buttons.reply import make_reply_branches, main_page_buttons
from bot.states import BranchesStates, BackStates
from bot.utils_function import get_address_from_location, find_nearest_branch, set_state_with_history

branch_router = Router()
BRANCHES = [
    ("Filial 1 - Vakzal", 41.3525, 69.2412),
    ("Filial 2 - Charxiy", 41.2853, 69.2034),
    ("Filial 3 - Navoiy", 41.2302, 69.2020),
    ("Filial 4 - Garadok", 41.2973, 69.2635),
]

@branch_router.message(F.text == "Filiallar 🏠")
async def branches_handler(message: Message, state: FSMContext):
    await state.set_state(BranchesStates.main)
    await message.answer("Filiallardan birini tanlang:", reply_markup=make_reply_branches())


@branch_router.message(BranchesStates.main, F.text == "Buyurtma berish")
async def branches_handler(message: Message, state: FSMContext):
    await set_state_with_history(state, BackStates.main_page)
    await message.answer("Siz asosiy menuga qaydingiz", reply_markup=main_page_buttons())


@branch_router.message(BranchesStates.main, F.location)
async def handle_user_location_nearest_branch(message: Message):

    lat_ = message.location.latitude
    lon_ = message.location.longitude

    nearest_branch = find_nearest_branch(lat_, lon_)
    if nearest_branch:
        name, b_lat, b_lon, distance = nearest_branch
        await message.answer(
            f"✅ Eng yaqin filial: {name}\n📍 Masofa: {distance:.2f} km"
        )
        await message.answer_location(latitude=b_lat, longitude=b_lon)
        # optional: return state to main menu

@branch_router.message(BranchesStates.main, F.text == "Vakzal")
async def send_vokzal_branch_location(message: Message,):
    for name, lat, lon in BRANCHES:
        if "Vakzal" in name:
            await message.answer(f"{name} manzili:")
            await message.answer_location(latitude=lat, longitude=lon)
            return


@branch_router.message(BranchesStates.main, F.text == "Charxiy")
async def send_charxiy_branch_location(message: Message):
    for name, lat, lon in BRANCHES:
        if "Charxiy" in name:
            await message.answer(f"{name} manzili:")
            await message.answer_location(latitude=lat, longitude=lon)
            return


@branch_router.message(BranchesStates.main, F.text == "Navoiy")
async def send_navoiy_branch_location(message: Message):
    for name, lat, lon in BRANCHES:
        if "Navoiy" in name:
            await message.answer(f"{name} manzili:")
            await message.answer_location(latitude=lat, longitude=lon)
            return


@branch_router.message(BranchesStates.main, F.text == "Garadok")
async def send_garadok_branch_location(message: Message):
    for name, lat, lon in BRANCHES:
        if "Garadok" in name:
            await message.answer(f"{name} manzili:")
            await message.answer_location(latitude=lat, longitude=lon)
            return

