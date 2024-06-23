import logging
import asyncio
import config
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.utils.keyboard import InlineKeyboardBuilder

API_TOKEN = config.token

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN, default=DefaultBotProperties(
        parse_mode=ParseMode.HTML
    ))
dp = Dispatcher()


@dp.message(Command(commands=['start']))
async def send_welcome(message: Message):
    await message.answer(f"Привет, <b>{message.from_user.first_name}</b>! \n"
                         f"Я эхобот. Пришли мне сообщение, и я его повторю. \n"
                         f"Для тебя есть несколько доступных команд:\n"
                         f"/help - вывод справочной информации\n"
                         f"/shop - Каталог товаров"
                         f"\n/echo - Повторяет сообщение\n"
                         )
@dp.callback_query(F.data == "help")
async def send_random_value(callback: types.CallbackQuery):
    await callback.message.answer("Я рад тебе помочь!")
    await callback.answer()


@dp.message(Command(commands=['help']))
async def command1(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Мне помогло!",
        callback_data="help"),
   await message.answer(f"Тут какой-то поясняющий текст, <b>{message.from_user.username}</b>", reply_markup=builder.as_markup())
    )
@dp.callback_query(F.data == "echo")
async def send_random_value(callback: types.CallbackQuery):
    await callback.message.answer("Бла-бла-бла-бла-бла-бла-бла-бла")
    await callback.answer()
@dp.message(Command(commands=['shop']))
async def command2(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="Магазин", callback_data="shop")),

    await message.answer("Типа список товаров", reply_markup=builder.as_markup())

@dp.callback_query(F.data  ==  "shop")
async def send_random_value(callback: types.CallbackQuery):
    await callback.message.answer("Перечень товаров магазина")
    await callback.answer()
@dp.callback_query(F.data  ==  "shop")
async def send_random_value(callback: types.CallbackQuery):
    await callback.message.answer("Перечень товаров магазина")
    await callback.answer()
@dp.message(F.text)
async def echo(message: types.Message):
    await message.answer(message.text)
@dp.message(Command(commands=['info']))
async def command4(message: types.Message):
    await message.answer("Какая-то информация"
                         "Ща мы напишем что-нибудь более интересное")
@dp.callback_query(F.data == "info")
async def send_info(message: types.Message):
    await message.answer()
async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
