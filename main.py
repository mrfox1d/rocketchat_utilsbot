from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
import os
from handlers import get_all_routers
import asyncio

load_dotenv()
TK = os.getenv('TOKEN')

bot = Bot(token=TK)
dp = Dispatcher()

async def main():
    dp.include_routers(*get_all_routers("handlers"))
    print("Бот запускается")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())