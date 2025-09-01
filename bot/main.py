# pyproject.toml: aiogram>=3.4
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from routers.user import user_router
import asyncio
import logging

bot = Bot("8333896356:AAERB58Gb6k6scltmwf25j053nShy49NySo")
dp = Dispatcher(storage=MemoryStorage())


dp.include_router(user_router)

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
