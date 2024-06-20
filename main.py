import logging
import asyncio
import config
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message

API_TOKEN = config.token

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()


@dp.message(Command(commands=['start']))
async def send_welcome(message: Message):
    await message.answer("Привет! Я эхобот. Пришли мне сообщение, и я его повторю.")


@dp.message(Command(commands=['help']))
async def command1(message: types.Message):
    await message.answer("Тут какой-то поясняющий текст")


@dp.message(Command(commands=['shop']))
async def command2(message: types.Message):
    await message.answer("Типа список товаров")


@dp.message(F.text)
async def echo(message: types.Message):
    await message.answer(message.text)


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
