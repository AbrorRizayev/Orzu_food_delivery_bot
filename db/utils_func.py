from aiogram.types import Message

from bot.buttons.reply import main_page_buttons

from db.models import User



async def save_user(user_id: int, name: str, phone_number: str):
    exist_user = await User.get(user_id)

    if exist_user:
        await User.update(user_id, first_name=name, phone_number=phone_number)
    else:
        await User.create(
            id=user_id,
            first_name=name,
            phone_number=phone_number
        )

async def check_user(message : Message):
    telegram_id = message.from_user.id
    user = await User.get(telegram_id)
    if user:
        await message.answer("Asosiy menuga hush kelibsiz", reply_markup=main_page_buttons())



