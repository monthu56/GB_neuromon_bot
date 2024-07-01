from aiogram import types

bt_start = types.KeyboardButton(text="Начать", request_contact=True)
bt_cancel = types.KeyboardButton(text="Отмена")

keyboard1=[
    [bt_start],
    [bt_cancel],
]

kb1 = types.ReplyKeyboardMarkup(keyboard=keyboard1, resize_keyboard=True)


