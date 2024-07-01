from aiogram import types

bt_start = types.KeyboardButton(text="Начать")
bt_cancel = types.KeyboardButton(text="Отмена")
bt_choise = types.KeyboardButton(text="Выбрать тур")
bt_register = types.KeyboardButton(text="Зарегистрироваться")

keyboard1=[
    [bt_choise]
]

kb1 = types.ReplyKeyboardMarkup(keyboard=keyboard1, resize_keyboard=True)

bt_number = types.KeyboardButton(text="Введите Ваш номер телефона")

keyboard2=[
    [bt_register],
]

kb2 = types.ReplyKeyboardMarkup(keyboard=keyboard2, resize_keyboard=True)

bt_choise_group = types.KeyboardButton(text="Групповой")
bt_choise_individual = types.KeyboardButton(text="Индивидуальный")

keyboard3=[
    [bt_choise_group],
    [bt_choise_individual],
]

kb3 = types.ReplyKeyboardMarkup(keyboard=keyboard3, resize_keyboard=True)

bt_island = types.KeyboardButton(text="Сахалин")
bt_island2 = types.KeyboardButton(text="Итуруп")
bt_island3 = types.KeyboardButton(text="Кунашир")
bt_island4 = types.KeyboardButton(text='Шикотан')

keyboard4=[
    [bt_island],
    [bt_island2],
    [bt_island3],
]

kb4 = types.ReplyKeyboardMarkup(keyboard=keyboard4, resize_keyboard=True)


