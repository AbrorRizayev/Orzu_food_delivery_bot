


from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_quantity_keyboard(quantity: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="➖", callback_data="decrease"),
            InlineKeyboardButton(text=str(quantity), callback_data="noop"),
            InlineKeyboardButton(text="➕", callback_data="increase"),
        ],
        [
            InlineKeyboardButton(text="🛒 Savatga qo'shish", callback_data="add_to_cart"),
        ]
    ])


def continue_shop_markup():
    ikb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Buyurtmani davom ettirish", callback_data="continue_savat")],
            [InlineKeyboardButton(text="Buyurtma berish", callback_data="order")],
            [InlineKeyboardButton(text="Savatni tozalash 🔄", callback_data="clear")]
        ]
    )
    return ikb


# order_id: int, {order_id}
def get_order_admin_markup():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Qabul qilindi", callback_data=f"accept_order:"),
            InlineKeyboardButton(text="❌ Bekor qilindi", callback_data=f"cancel_order:")
        ]
    ])

