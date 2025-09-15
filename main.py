# pyproject.toml: aiogram>=3.4
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from routers.user import user_router
import asyncio
import logging
from utils.drive import service

bot = Bot("8419104447:AAFqBRb6pXMZV3NDIA5YlJyRhpvZtow7sb8")
dp = Dispatcher(storage=MemoryStorage())



dp.include_router(user_router)

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
