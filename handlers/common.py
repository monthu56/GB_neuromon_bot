import asyncio
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.client.default import DefaultBotProperties
from keyboards.keyboard import kb1
from utils.database import add_user

router = Router()

@router.message(Command("tour"))
async def start(message: types.Message):
    await add_user(message.from_user.id, message.from_user.username)
    await message.answer(f"Привет, {message.from_user.full_name}!")
    await message.answer(f"Я бот, который поможет тебе с выбором тура на Сахалин!")
    await message.answer(f"Чтобы начать выбор тура, нажми на кнопку ниже", reply_markup=kb1)




