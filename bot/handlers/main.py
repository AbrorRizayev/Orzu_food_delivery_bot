from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from bot.buttons.reply import make_reply_keyboard, get_location_markup, main_page_buttons
from bot.handlers.menu import WhateverForm
from bot.states import BackStates, RegisterStates
from bot.utils_function import set_state_with_history, get_address_from_location, find_nearest_branch
from db.models import User
from db.utils_func import save_user, check_user

main_router = Router()
size = 2


@main_router.message(CommandStart())
async def name_handler(message: Message, state: FSMContext):
    telegram_id = message.from_user.id
    user_first_name = message.from_user.first_name
    user = await User.get(telegram_id)
    if user:
        await message.answer("Asosiy menuga hush kelibsiz", reply_markup=main_page_buttons())
    else:
        await state.update_data(first_name=user_first_name)
        rkb = ReplyKeyboardBuilder()
        rkb.add(KeyboardButton(text="📞 Telefon raqamni yuborish", request_contact=True))
        await message.answer(
            "📱 Telefon raqamingizni yuboring:",
            reply_markup=rkb.as_markup(resize_keyboard=True)
        )
        await set_state_with_history(state, RegisterStates.phone)





@main_router.message(F.contact,RegisterStates.phone)
async def main_page_handler(message: Message, state: FSMContext):

    data = await state.get_data()
    user_id = message.from_user.id
    name = data.get("first_name")
    phone_number = message.contact.phone_number

    await save_user(user_id, name, phone_number)


    buttons = ["Biz haqimizda ℹ️", "Buyurtma berish 🛒", "Buyurtmalarim 📃", "Filiallar 🏠", "Sozlamalar ⚙️"]
    markup_ = make_reply_keyboard(buttons, size)
    await set_state_with_history(state, BackStates.main_page)
    await message.answer("Kerakli bo‘limni tanlang:", reply_markup=markup_)







@main_router.message(F.text == "Sozlamalar ⚙️")
async def sozlamalar_handler(message: Message, state: FSMContext):
    buttons = ["Ismni o'zgartirish", "Telefon raqmni ozgartirish", "Orqaga"]
    markup_ = make_reply_keyboard(buttons, size)
    data = await state.get_data()
    print(data)
    await set_state_with_history(state, BackStates.main_page)
    await message.answer("Kerakli bo'limni tanlang", reply_markup=markup_)




@main_router.message(F.text == "Telefon raqmni ozgartirish")
async def telefon_raqam_change_handler(message: Message, state: FSMContext):
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="📱 Telefon raqamni yuborish", request_contact=True))

    await message.answer("📱 Iltimos, yangi telefon raqamingizni yuboring:Masalan(+998*********)",
                         reply_markup=builder.as_markup(resize_keyboard=True))
    await state.set_state(RegisterStates.change_phone)



@main_router.message(RegisterStates.change_phone, F.contact)
async def receive_new_phone(message: Message, state: FSMContext):
    phone = message.contact.phone_number
    tg_id = message.from_user.id
    user = (await User.filter(telegram_id=tg_id)).first()
    if user:
        user.phone_number = phone
        await User.update(user.id, phone_number=phone)
        await message.answer("✅ Telefon raqam muvaffaqiyatli yangilandi.")



@main_router.message(F.text == "Buyurtma berish 🛒")
async def buy_button_handler(message: Message, state: FSMContext):
    buttons = ["Yetkazib berish", "Olib ketish", "Orqaga"]
    markup_ = make_reply_keyboard(buttons, size)
    data = await state.get_data()
    print(data)
    await set_state_with_history(state, BackStates.del_status)
    await message.answer("Mahsulot yetkazish turini tanlang:", reply_markup=markup_)


@main_router.message(F.text.in_(["Olib ketish", "Yetkazib berish"]))
async def delivery_type_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    await state.update_data(del_status=message.text)
    await set_state_with_history(state, BackStates.location)

    await message.answer("Geo-joylashuvingizni yuboring:", reply_markup=get_location_markup())




@main_router.message(BackStates.location, F.location)
async def handle_user_location(message: Message, state: FSMContext):
    lat = message.location.latitude
    lon = message.location.longitude

    address = await get_address_from_location(lat, lon)
    buttons = ["Yoq ❎", "Ha ✅"]
    markup_ = make_reply_keyboard(buttons, size)
    data = await state.get_data()
    print(data)
    await state.update_data(lat=lat, lon=lon)
    await message.answer(f"📍 Buyurtma qilmoqchi manzilingiz:\n\n{address}")
    await message.answer("📍 Ushbu manzilni tasdiqlaysizmi?", reply_markup=markup_)


@main_router.message(F.text == "Ha ✅")
async def confirm_location(message: Message, state: FSMContext):
    data = await state.get_data()
    lat = data.get("lat")
    lon = data.get("lon")
    if lat is None or lon is None:
        return await message.answer("❗ Location topilmadi, iltimos qayta yuboring.")

    nearest_branch = find_nearest_branch(lat, lon)
    if not nearest_branch:
        return await message.answer("❗ Filial topilmadi.")

    name, b_lat, b_lon, distance = nearest_branch
    await state.update_data(branch=name)

    await message.answer(
        f"✅ Eng yaqin filial: {name}\n📍 Masofa: {distance:.2f} km"
    )
    await message.answer_location(latitude=b_lat, longitude=b_lon)
    buttons = ["Savat 🛒", "Tico", "Damas", "Matiz", "Nexia", "Cobalt", "Captiva", "Gentra", "Malibu", "Gelik"]
    markup = make_reply_keyboard(buttons, size)
    await set_state_with_history(state, BackStates.product_)
    await message.answer("Buyurtma qilmoqchi bolgan mahsulotingizni tanlang 😊", reply_markup=markup)
    await state.set_state(WhateverForm.food)


@main_router.message(F.text == "Yoq ❎")
async def cancel_location(message: Message, state: FSMContext):
    await message.answer("❌ Manzil tasdiqlanmadi. Iltimos qaytadan to‘g‘ri manzil yuboring.")
    await state.set_state(BackStates.location)
    await message.answer("📍 Geo-joylashuvni yuboring:", reply_markup=get_location_markup())









# ============================= BACK uchun ==========================================
@main_router.message(F.text == "Orqaga")
async def go_back_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    history = data.get("state_history", [])

    if not history:
        await message.answer("🔙 Orqaga qaytib bo‘lmadi.")
        return

    prev_state = history.pop()
    await state.update_data(state_history=history)
    await state.set_state(prev_state)

    if prev_state == BackStates.main_page:
        markup_ = make_reply_keyboard(["Biz haqimizda ℹ️",
                                       "Buyurtma berish 🛒",
                                       "Buyurtmalarim 📃",
                                       "Filiallar 🏠",
                                       "Sozlamalar ⚙️"], size)
        await message.answer("🏠 Asosiy menyu", reply_markup=markup_)

    elif prev_state == BackStates.del_status:
        markup_ = make_reply_keyboard(["Yetkazib berish", "Olib ketish", "Orqaga"], size)
        await message.answer("📦 Yetkazish turini tanlang", reply_markup=markup_)

    elif prev_state == BackStates.location:
        await message.answer("📍 Iltimos geo-joylashuv yuboring:", reply_markup=get_location_markup())

    elif prev_state == BackStates.category_:
        await message.answer("📚 Kategoriya sahifasi.")

    elif prev_state == BackStates.product_:
        await message.answer("🛒 Mahsulotlar sahifasi.")

    else:
        await message.answer("⬅️ Oldingi sahifaga qaytdik.")
