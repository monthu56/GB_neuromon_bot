from aiogram import Router, types, F
from aiogram.filters import Command
import config
from keyboards.keyboard import kb1, kb3, kb4, kb2
from utils.database import add_user
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from main import bot

router = Router()
adminID = config.adminID

# Состояния для выбора тура
class ChooseTour(StatesGroup):
    grade = State()
    tour = State()
    start = State()
    number = State()

# Обработчик команды /start
@router.message(Command("start"))
async def start(message: types.Message):
    await message.answer_photo(photo='https://www.na-sakhalin.ru/storage/uploads/tours/gallery/fullsize/d45d72cb5bccb1251aa2c4b64fda5955.jpeg',
                               caption=f'Привет, {message.from_user.full_name}!'
                               f'\nЯ бот, который поможет тебе с выбором тура на Сахалин!'
                               f'\nДля начала тебе нужно зарегистрироваться', reply_markup=kb2)


# Обработчик текста 'зарегистрироваться'
@router.message(F.text.lower() == 'зарегистрироваться')
async def enter_number(message: types.Message, state: FSMContext):
    await message.answer(f"Пожалуйста, введите ваш номер телефона (только цифры)", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(ChooseTour.number)

# Обработчик ввода номера телефона
@router.message(ChooseTour.number)
async def process_number(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(number=message.text)
        await add_user(message.from_user.id, message.from_user.username, message.text)
        await message.answer(f"Вы успешно зарегистрировались!", reply_markup=kb1)
        await bot.send_message(adminID, f"Пользователь {message.from_user.full_name} зарегистрировался с номером телефона: {message.text}")
        await state.set_state(ChooseTour.start)

# Обработчик текста 'выбрать тур'
@router.message(ChooseTour.start, F.text.lower() == 'выбрать тур')
async def choose_tour(message: types.Message, state: FSMContext):
    await message.answer(f"Какой формат тура Вам подходит?", reply_markup=kb3)
    await state.set_state(ChooseTour.grade)

# Обработчик выбора группового тура
@router.message(ChooseTour.grade, F.text.lower() == 'групповой')
async def group_tour(message: types.Message, state: FSMContext):
    await state.update_data(grade=message.text)
    await message.answer(f"Вы выбрали групповой тур")
    await message.answer(f"Выберите остров, который хотите посетить:", reply_markup=kb4)
    await state.set_state(ChooseTour.tour)

# Обработчик выбора индивидуального тура
@router.message(ChooseTour.grade, F.text.lower() == 'индивидуальный')
async def individual_tour(message: types.Message, state: FSMContext):
    await state.update_data(grade=message.text)
    await message.answer(f"Вы выбрали индивидуальный тур")
    await message.answer(f"Выберите остров, который хотите посетить:", reply_markup=kb4)
    await state.set_state(ChooseTour.tour)

# Обработчик выбора острова
@router.message(ChooseTour.tour)
async def process_tour(message: types.Message, state: FSMContext):
    current_state = await state.get_data()
    user_data = await state.get_data()
    await message.answer(f"Отлично! Вы выбрали {current_state['grade']} тур на {message.text}!")
    await message.answer(f"Приятного путешествия!", reply_markup=types.ReplyKeyboardRemove())
    await bot.send_message(adminID, f"Пользователь {message.from_user.full_name}, с номером {user_data['number']} выбрал {current_state['grade']} тур на {message.text}!")
    await state.clear()
