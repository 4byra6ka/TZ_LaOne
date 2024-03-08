import os
import sys

from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

import asyncio

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

import database
import handlers
from database import Base


async def main():
    load_dotenv('.env')
    engine = create_async_engine(url=str(os.getenv('URL_POSTGRESQL')), echo=True)
    sessionmaker = async_sessionmaker(engine, expire_on_commit=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    bot = Bot(str(os.getenv('API_KEY_TG')))
    dp = Dispatcher(storage=MemoryStorage())
    dp.update.middleware(database.DbSessionMiddleware(session_pool=sessionmaker))
    dp.include_router(handlers.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
