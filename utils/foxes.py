from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
import requests

async def command_fox(message: types.Message):
    img_fox = fox()
    builder = InlineKeyboardBuilder()
    builder.add(
        types.InlineKeyboardButton(
            text="Еще одна лиса!",
            callback_data="more_fox"
        )
    )
    await message.answer("Вот тебе лиса!")
    await message.answer_photo(img_fox, reply_markup=builder.as_markup())
def fox():
    url = 'https://randomfox.ca/floof/'
    response = requests.get(url)
    if response.status_code:
        data = response.json()
        return(data.get('image'))