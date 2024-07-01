import logging
import asyncio
import config
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import CallbackQuery
from aiogram.enums import ParseMode
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.client.default import DefaultBotProperties
from keyboards.keyboard import kb1
from utils.foxes import fox
from utils.database import add_user

# Конфигурация токена
API_TOKEN = config.token

# Настройка логирования
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

# Создание бота и диспетчера
bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


# Обработчик команды /start
@dp.message(Command(commands=['start']))
async def send_welcome(message: types.Message):
    logger.info(f"Получено сообщение от {message.from_user.username}: {message.text}")
    builder = InlineKeyboardBuilder()
    builder.add(
        types.InlineKeyboardButton(
            text="Зарегистрироваться",
            callback_data="register"
        )
    )
    await message.answer(
        f"Привет, <b>{message.from_user.first_name}</b>! \n"
        "Я эхобот. Пришли мне сообщение, и я его повторю. \n"
        "Для тебя есть несколько доступных команд:\n"
        "/help - вывод справочной информации\n"
        "/shop - Каталог товаров\n",
        reply_markup=builder.as_markup()
    )

@dp.message(F.text.lower() == 'ура')
async def send_ura(message: types.Message):
    await message.answer(f'Ура!')
# Обработчик callback для "register"
@dp.callback_query(F.data == "register")
async def register_callback(callback: CallbackQuery):
    logger.info(f"Пользователь {callback.from_user.username} нажал кнопку 'Зарегистрироваться'")
    await add_user(callback.from_user.id, callback.from_user.username)  # Call the save_user function
    await callback.message.answer("Спасибо за регистрацию!")
    await callback.answer()

# Обработчик команды /fox
@dp.message(Command(commands=['fox']))
async def command_fox(message: types.Message):
    logger.info(f"Получено сообщение от {message.from_user.username}: {message.text}")
    img_fox = fox()
    builder = InlineKeyboardBuilder()
    builder.add(
        types.InlineKeyboardButton(
            text="{Хочу ещё!}",
            callback_data="more_fox"
        )
    )
    await message.answer("Вот тебе лиса!")
    await message.answer_photo(img_fox, reply_markup=builder.as_markup())



# Обработчик callback для "more_fox"
@dp.callback_query(F.data == "more_fox")
async def more_fox_callback(callback: CallbackQuery):
    logger.info(f"Пользователь {callback.from_user.username} нажал кнопку 'Еще одна лиса!'")
    img_fox = fox()
    builder = InlineKeyboardBuilder()
    builder.add(
        types.InlineKeyboardButton(
            text="Хочу ещё!",
            callback_data="more_fox"
        )
    )
    await callback.message.answer_photo(img_fox, reply_markup=builder.as_markup())
    await callback.answer()


# Обработчик команды /help
@dp.message(Command(commands=['help']))
async def command_help(message: types.Message):
    logger.info(f"Получено сообщение от {message.from_user.username}: {message.text}")
    builder = InlineKeyboardBuilder()
    builder.add(
        types.InlineKeyboardButton(
            text="Мне помогло!",
            callback_data="help"
        )
    )
    await message.answer(
        f"Тут какой-то поясняющий текст, <b>{message.from_user.username}</b>",
        reply_markup=builder.as_markup()
    )
# Обработчик callback для "help"
@dp.callback_query(F.data == "help")
async def help_callback(callback: CallbackQuery):
    logger.info(f"Пользователь {callback.from_user.username} нажал кнопку 'Мне помогло!'")
    await callback.message.answer("Рад, что помог!")
    await callback.answer()
# Обработчик команды /pls
@dp.message(Command(commands=['pls']))
async def command_pls(message: types.Message):
    logger.info(f"Получено сообщение от {message.from_user.username}: {message.text}")
    await message.answer(
        "Вызовите эту команду, если вам нужна помощь или есть вопросы. \n"
        "Например: /help - для получения справочной информации \n"
        "         /shop - для просмотра каталога товаров", reply_markup=kb1
    )
    # Remove the keyboard markup after sending the message
    await message.edit_reply_markup(reply_markup=None)
# Обработчик команды /shop
@dp.message(Command(commands=['shop']))
async def command_shop(message: types.Message):
    logger.info(f"Получено сообщение от {message.from_user.username}: {message.text}")
    builder = InlineKeyboardBuilder()
    builder.add(
        types.InlineKeyboardButton(
            text="Товар 1",
            callback_data="item_1"
        ),
        types.InlineKeyboardButton(
            text="Товар 2",
            callback_data="item_2"
        )
    )
    await message.answer(
        "Каталог товаров:",
        reply_markup=builder.as_markup()
    )

# Обработчики для товаров
@dp.callback_query(F.data == "item_1")
async def item_1(callback: CallbackQuery):
    logger.info(f"Пользователь {callback.from_user.username} выбрал Товар 1")
    await callback.message.answer("Описание Товара 1")
    await callback.answer()

@dp.callback_query(F.data == "item_2")
async def item_2(callback: CallbackQuery):
    logger.info(f"Пользователь {callback.from_user.username} выбрал Товар 2")
    await callback.message.answer("Описание Товара 2")
    await callback.answer()
# Обработчик команды /lot
@dp.message(Command(commands=['lot']))
async def command_lot(message: types.Message):
    logger.info(f"Получено сообщение от {message.from_user.username}: {message.text}")
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(text="1", callback_data="lot_1"),
        types.InlineKeyboardButton(text="2", callback_data="lot_2")
    )
    builder.row(
        types.InlineKeyboardButton(text="3", callback_data="lot_3"),
        types.InlineKeyboardButton(text="4", callback_data="lot_4")
    )
    await message.answer(
        "Выберите лот:",
        reply_markup=builder.as_markup()
    )

# Обработчики для лотов
@dp.callback_query(F.data.startswith("lot_"))
async def lot_callback(callback: CallbackQuery):
    lot_number = callback.data.split("_")[1]
    logger.info(f"Пользователь {callback.from_user.username} выбрал лот {lot_number}")
    await callback.message.answer(f"Вы выбрали лот {lot_number}")
    await callback.answer()
# Обработчик текстовых сообщений
@dp.message()
async def echo(message: types.Message):
    logger.info(f"Получено сообщение от {message.from_user.username}: {message.text}")
    await message.answer(message.text)

# Функция запуска polling
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
