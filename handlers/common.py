from aiogram import Router, types, F
from aiogram.filters import Command
import config
from keyboards.keyboard import kb1, kb3, kb4
from utils.database import add_user
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from main import bot
from config import adminID
router = Router()

adminID = config.adminID
class ChooseTour(StatesGroup):
    grade = State()
    tour = State()

class Number(StatesGroup):
    number = State()

@router.message(Command("start"))
async def start(message: types.Message):
    await message.answer(f"Привет, {message.from_user.full_name}!"),
    await message.answer(f"Я бот, который поможет тебе с выбором тура на Сахалин!"),
    await message.answer(f"Чтобы начать выбор тура, нажми на кнопку ниже", reply_markup=kb1)

@router.message(F.text.lower() == 'зарегистрироваться')
async def enter_number(message: types.Message, state: FSMContext):
    await message.answer(f"Пожалуйста введите ваш номер телефона (только цифры)")
    await state.set_state(Number.number)

@router.message(Number.number)
async def enter_number(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await add_user(message.from_user.id, message.from_user.username, message.text)
        await message.answer(f"Вы успешно зарегистрировались!")
        await bot.send_message(adminID, f"Пользователь {message.from_user.full_name} зарегистрировался с номером телефона: {message.text}")
        await state.finish()
    else:
        await message.answer(f"Пожалуйста, введите только цифры.")
@router.message(F.text.lower() == 'выбрать тур')
async def choose_lot(message: types.Message, state: FSMContext):
    await message.answer(f"Какой формат тура Вам подходит?", reply_markup=kb3)
    await state.set_state(ChooseTour.grade)

@router.message(ChooseTour.grade, F.text.lower() == 'групповой')
async def group_lot(message: types.Message, state: FSMContext):
    await state.update_data(grade=message.text.lower())
    await message.answer(f"Вы выбрали групповой тур")
    await message.answer(f"Выберите остров который хотите посетить:", reply_markup=kb4)
    await state.set_state(ChooseTour.tour)

@router.message(ChooseTour.grade, F.text.lower() == 'индивидуальный')
async def individual_lot(message: types.Message, state: FSMContext):
    await state.update_data(grade=message.text.lower())
    await message.answer(f"Вы выбрали индивидуальный тур")
    await message.answer(f"Выберите остров который хотите посетить:", reply_markup=kb4)
    await state.set_state(ChooseTour.tour)


@router.message(ChooseTour.tour)
async def sakhalin_lot(message: types.Message, state: FSMContext):
    current_state = await state.get_data()
    await message.answer(f"Отлично! Вы выбрали {current_state['grade']} тур на {message.text}!")
    await message.answer(f"Приятного путешествия!", reply_markup=types.ReplyKeyboardRemove())



