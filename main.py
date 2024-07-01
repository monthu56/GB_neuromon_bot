import logging
import asyncio
import config
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from handlers import common

API_TOKEN = config.token
bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
async def main():
    logging.basicConfig(level=logging.INFO)
    dp = Dispatcher()
    dp.include_router(common.router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
