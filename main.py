import logging
import asyncio
import config
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.enums import ParseMode
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.client.default import DefaultBotProperties

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
async def send_welcome(message: Message):
    logger.info(f"Получено сообщение от {message.from_user.username}: {message.text}")
    await message.answer(
        f"Привет, <b>{message.from_user.first_name}</b>! \n"
        "Я эхобот. Пришли мне сообщение, и я его повторю. \n"
        "Для тебя есть несколько доступных команд:\n"
        "/help - вывод справочной информации\n"
        "/shop - Каталог товаров\n"
        "/echo - Повторяет сообщение\n"
    )

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
