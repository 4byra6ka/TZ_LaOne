from datetime import datetime
from typing import Callable, Awaitable, Dict, Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, BigInteger, DateTime, Boolean

Base = declarative_base()


class WB(Base):
    __tablename__ = "wb"

    id = Column(Integer, primary_key=True)
    tg_user_id = Column(BigInteger)
    created_on = Column(DateTime, default=datetime.now)
    wb_id = Column(BigInteger)
    task = Column(Boolean, default=False)


class DbSessionMiddleware(BaseMiddleware):
    def __init__(self, session_pool: async_sessionmaker):
        super().__init__()
        self.session_pool = session_pool

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        async with self.session_pool() as session:
            data["session"] = session
            return await handler(event, data)
