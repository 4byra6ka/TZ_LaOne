import asyncio
import os
import sys

from aiogram import Bot
from celery import Celery
from celery.schedules import crontab
from dotenv import load_dotenv
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from database import Base, WB
from services import wb_api

load_dotenv('.env')
celery_app = Celery('tasks', broker=str(os.getenv('URL_REDIS')))
celery_app.autodiscover_tasks()
celery_app.conf.broker_connection_retry_on_startup = True
celery_app.conf.beat_schedule = {
    "add-every-5-minutes": {
        "task": "worker_celery.task",
        "schedule": crontab(minute='*/5'),
    },
}
celery_app.conf.update(timezone="Europe/Moscow")


@celery_app.task
def task():
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(wb_task())


async def wb_task() -> None:
    bot = Bot(str(os.getenv('API_KEY_TG')))
    engine = create_async_engine(url=str(os.getenv('URL_POSTGRESQL')), echo=False)
    sessionmaker = async_sessionmaker(engine, expire_on_commit=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with sessionmaker() as session:
        db_query = await session.execute(select(WB).where(WB.task == True))
        for data in db_query.scalars():
            print(f"id: {data.id} | tg_user_id: {data.tg_user_id}")
            wb_data = await wb_api(data.wb_id)
            await bot.send_message(chat_id=data.tg_user_id, text=f'Название: {wb_data["name"]}\n'
                                                                 f'Артикул: {wb_data["id"]}\n'
                                                                 f'Цена: {int(wb_data["salePriceU"]) / 100}руб\n'
                                                                 f'Рейтинг товара: {wb_data["supplierRating"]}\n'
                                                                 f'Количество товара: {wb_data["stocks"]}\n'
                                   )
