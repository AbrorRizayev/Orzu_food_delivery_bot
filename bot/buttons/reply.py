from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder




def make_reply_keyboard(buttons: list[str], row_width: int) -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=btn) for btn in buttons[i:i+row_width]]
            for i in range(0, len(buttons), row_width)
        ],
        resize_keyboard=True,
        # one_time_keyboard=False
    )
    return markup


def product_menu():
    buttons = ["Savat 🛒", "Tico", "Damas", "Matiz", "Nexia", "Cobalt", "Captiva", "Gentra", "Malibu", "Gelik"]
    size =2
    markup_=make_reply_keyboard(buttons, size)
    return markup_

def make_reply_branches():
    rkb = ReplyKeyboardBuilder()
    rkb.add(KeyboardButton(text="📍 Eng yaqin filialni topish", request_location=True),
            KeyboardButton(text="Charxiy"),
            KeyboardButton(text="Vakzal"),
            KeyboardButton(text="Navoiy"),
            KeyboardButton(text="Garadok"),
            KeyboardButton(text="Buyurtma berish"))
    rkb.adjust(1,2,2,1, repeat=True)
    return rkb.as_markup(resize_keyboard=True)



def main_page_buttons() -> ReplyKeyboardMarkup:
    buttons = ["Biz haqimizda ℹ️", "Buyurtma berish 🛒", "Buyurtmalarim 📃", "Filiallar 🏠", "Sozlamalar ⚙️"]
    size = 2
    res = make_reply_keyboard(buttons, size)
    return res



def get_location_markup():
    rkb = ReplyKeyboardBuilder()
    rkb.add(
        KeyboardButton(text="📍 Geo-joylashuvni yuborish", request_location=True),
        KeyboardButton(text="Orqaga")
    )
    rkb.adjust(1, 1)
    return rkb.as_markup(resize_keyboard=True)

