from aiogram import Router, F, Bot
from re import Match
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, FSInputFile, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, \
    ReplyKeyboardRemove

from bot.buttons.inline import get_quantity_keyboard, continue_shop_markup, get_order_admin_markup
from bot.buttons.reply import product_menu, make_reply_keyboard
from bot.states import BackStates
from bot.utils_function import set_state_with_history
from db.models import Product, User
from environment.utils import Env

menu_router = Router()

size = 2

class WhateverForm(StatesGroup):
    food = State()

bot = Bot(token=Env.bot.TOKEN)
@menu_router.message(WhateverForm.food, F.text.regexp(r'^(\w+)$').as_("regex_food"))
async def show_product_by_name(message: Message, state: FSMContext, regex_food: Match):
    product_name = regex_food.group(1)

    old_data = await state.get_data()
    old_msg_id = old_data.get("message_id")
    if old_msg_id:
        try:
            await bot.delete_message(chat_id=message.chat.id, message_id=old_msg_id)
        except:
            pass

    product = await Product.get_by_name(name=product_name)
    if not product:
        await message.answer("❌ Mahsulot topilmadi.", reply_markup=ReplyKeyboardRemove())
        return

    count = 1
    total_price = product.price * count

    caption = (
        f"<b>{product.name}</b>\n\n"
        f"{product.description}\n\n"
        f"{product.name} {product.price} x {count} = <b>{total_price}</b>\n"
        f"<b>Umumiy:</b> {total_price} UZS"
    )

    photo_message = await message.answer_photo(
        photo=FSInputFile(product.photo),
        caption=caption,
        reply_markup=get_quantity_keyboard(quantity=count),
        parse_mode="HTML"
    )

    await state.update_data(
        quantity=count,
        title=product.name,
        description=product.description,
        price=product.price,
        photo=product.photo,
        message_id=photo_message.message_id
    )



@menu_router.callback_query(WhateverForm.food ,F.data.in_(["increase", "decrease"]))
async def update_quantity(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    quantity = data.get("quantity", 1)
    price = data.get("price", 19000)
    title = data.get("title", "Gentra")
    description = data.get("description", "")
    message_id = data.get("message_id")
    chat_id = callback.message.chat.id

    if callback.data == "increase":
        quantity += 1
    elif callback.data == "decrease" and quantity > 1:
        quantity -= 1

    await state.update_data(quantity=quantity)

    total = quantity * price
    new_caption = (
        f"<b>{title}</b>\n\n"
        f"{description}\n\n"
        f"{title} {price} x {quantity} = <b>{total}</b>\n"
        f"<b>Umumiy:</b> {total} UZS"
    )

    await callback.bot.edit_message_caption(
        chat_id=chat_id,
        message_id=callback.message.message_id,
        caption=new_caption,
        reply_markup=get_quantity_keyboard(quantity),
        parse_mode="HTML"
    )

    await callback.answer()


@menu_router.callback_query(F.data == "noop")
async def noop_handler(callback: CallbackQuery):
    await callback.answer()


@menu_router.callback_query(F.data == "add_to_cart")
async def add_to_cart(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    title = data.get("title")
    price = data.get("price")
    quantity = data.get("quantity", 1)
    cart = data.get("cart", [])

    for item in cart:
        if item["title"] == title:
            item["quantity"] += quantity
            break
    else:
        cart.append({
            "title": title,
            "price": price,
            "quantity": quantity
        })

    await state.update_data(cart=cart, quantity=1)

    await callback.answer("Mahsulot savatga qo‘shildi!", show_alert=True,reply_markup=product_menu())



@menu_router.message(F.text == "Savat 🛒")
async def show_cart(message: Message, state: FSMContext):
    data = await state.get_data()
    cart = data.get("cart", [])

    if not cart:
        await message.answer("🛒 Savatingiz hozircha bo‘sh.")
        return

    total_sum = 0
    text = "🛒 <b>Savatingizdagi mahsulotlar:</b>\n\n"

    await state.set_state(WhateverForm.food)
    for i, item in enumerate(cart, start=1):
        title = item["title"]
        price = item["price"]
        quantity = item["quantity"]
        total = price * quantity
        total_sum += total
        text += (
            f"{i}. {title}\n"
            f"   Narx: {price} UZS × {quantity} = <b>{total}</b> UZS\n\n"
        )
    text += f"<b>Umumiy:</b> {total_sum} UZS"

    await message.answer(text, parse_mode="HTML", reply_markup=continue_shop_markup())




@menu_router.callback_query(F.data == "continue_savat")
async def continue_shop(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer(
        "Mahsulotlar bo‘limiga qaytdingiz",
        reply_markup=product_menu()
    )



@menu_router.callback_query(F.data == "clear")
async def clear(callback: CallbackQuery, state: FSMContext):
    await state.update_data(cart=[])  # Savatni bo'shatamiz
    await callback.answer("🧺 Savat tozalandi!", show_alert=True)
    await callback.message.edit_text("🛒 Savatingiz hozirda bo‘sh.")


@menu_router.callback_query(WhateverForm.food ,F.data == "order")
async def confirm_order(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    cart = data.get("cart", [])
    lat = data.get("lat")
    lon = data.get("lon")


    if not cart or not lat or not lon:
        await callback.answer("❗️ Buyurtma uchun savat va joylashuv kerak!", show_alert=True)
        return

    total = 0
    text = "🛒 <b>Buyurtmangiz:</b>\n\n"
    for i, item in enumerate(cart, 1):
        title = item["title"]
        price = item["price"]
        quantity = item["quantity"]
        item_total = price * quantity
        total += item_total
        text += f"{i}. {title} — {price} × {quantity} = <b>{item_total}</b> UZS\n"

    text += f"\n📍 <b>Joylashuv:</b> https://maps.google.com/?q={lat},{lon}"
    text += f"\n\n<b>Umumiy narx:</b> {total} UZS"

    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Buyurtmani tasdiqlash", callback_data="confirm_order")],
            [InlineKeyboardButton(text="Asosiy menuga qaytish ", callback_data="return_to_main_page")],
            [InlineKeyboardButton(text="🔙 Orqaga", callback_data="continue_savat")]
        ]
    )
    await callback.message.answer(
        text,
        parse_mode="HTML",
        reply_markup=markup)

    await callback.answer("zoor")




#     ==========================================SEND to ADMIN =============================

ADMIN_ID = 5080580890

@menu_router.callback_query(F.data == "confirm_order")
async def send_order_to_admin(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    cart = data.get("cart", [])
    lat = data.get("lat")
    lon = data.get("lon")
    branch = data.get("branch")
    del_status = data.get("del_status",)
    tg_id = callback.from_user.id

    users = await User.filter(id=tg_id)
    user = users[0] if users else None
    if user:
        phone_number = user.phone_number

    if not cart or not lat or not lon:
        await callback.answer("❗️ Buyurtma yetarli emas!", show_alert=True)
        return

    total = 0
    text = (
        f"🆕 <b>Yangi buyurtma</b>\n\n"
        f"👤 <b>Foydalanuvchi:</b> {callback.from_user.full_name}\n"
        f"📞 <b>Telefon raqam:</b> {phone_number}\n"
        f"📞 <b>Mahsulot qabul qilish turi:</b> {del_status}\n"
        f"🏠 <b>Tanlangan filial:</b> {branch}\n"
        f"📍 <b>Buyurtmachini joylashuvi:</b> https://maps.google.com/?q={lat},{lon}\n\n"
        "<b>Mahsulotlar:</b>\n"
    )

    for i, item in enumerate(cart, 1):
        title = item["title"]
        price = item["price"]
        quantity = item["quantity"]
        item_total = price * quantity
        total += item_total
        text += f"{i}. {title} — {price} × {quantity} = <b>{item_total}</b> UZS\n"

    text += f"\n<b>Umumiy narx:</b> {total} UZS"

    await callback.bot.send_message(ADMIN_ID, text, parse_mode="HTML", reply_markup=get_order_admin_markup())

    await callback.message.answer("✅ Buyurtmangiz qabul qilindi! Tez orada bog‘lanamiz.")
    await state.clear()
    await callback.answer()






#     ========================================== =============================

@menu_router.callback_query(F.data =="return_to_main_page")
async def food_handler(callback: CallbackQuery, state: FSMContext):
    buttons = ["Biz haqimizda ℹ️", "Buyurtma berish 🛒", "Buyurtmalarim 📃", "Filiallar 🏠", "Sozlamalar ⚙️"]
    markup_ = make_reply_keyboard(buttons, size)
    await set_state_with_history(state, BackStates.main_page)
    await callback.message.answer("Kerakli bo‘limni tanlang:", reply_markup=markup_)
    await callback.answer()


WORKER_GROUP_ID = -1001967494993

@menu_router.callback_query(F.data.startswith("accept_order:"))
async def handle_accept_order(callback: CallbackQuery):
    # order_id = int(callback.data.split(":")[1])
    order_text = callback.message.text

    await callback.bot.send_message(
        WORKER_GROUP_ID,
        f"📦 <b>Qabul qilingan buyurtma:</b>\n\n{order_text}",
        parse_mode="HTML"
    )

    await callback.message.edit_reply_markup(
        reply_markup=None
    )
    await callback.answer("Buyurtma ishchi guruhga yuborildi.")



@menu_router.callback_query(F.data.startswith("cancel_order:"))
async def handle_cancel_order(callback: CallbackQuery):
    # order_id = int(callback.data.split(":")[1])
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.answer("Buyurtma bekor qilindi.")





@menu_router.callback_query(F.data == "accept_order")
async def handle_accept_order(callback: CallbackQuery):
    order_text = callback.message.text

    await callback.bot.send_message(
        WORKER_GROUP_ID,
        f"📦 <b>Qabul qilingan buyurtma:</b>\n\n{order_text}",
        parse_mode="HTML"
    )
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.answer("✅ Buyurtma ishchi guruhga yuborildi.")




