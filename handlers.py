from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, Message, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from database import WB
from services import wb_api

router = Router()

menu_names = ["Получить информацию по товару", "Остановить уведомления", "Получить информацию из БД"]


class WB_State(StatesGroup):
    wb_id = State()


class WBCallback(CallbackData, prefix="wb"):
    wb: str
    id: int


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer(
        "WB бот",
        reply_markup=get_kb(menu_names)
    )


@router.message(Command("cancel"))
@router.message(F.text.casefold() == "cancel")
@router.callback_query(F.data == "cancel")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(text="Отмена ввода")


@router.message(F.text.in_(menu_names))
async def menu_chosen(message: Message, state: FSMContext, session: AsyncSession) -> None:
    if message.text == "Получить информацию по товару":
        builder = InlineKeyboardBuilder().add(InlineKeyboardButton(text="Отмена", callback_data="cancel"))
        await state.set_state(WB_State.wb_id)
        await message.answer(
            text="Введите артикул товара WB:",
            reply_markup=builder.as_markup()
        )
    elif message.text == "Остановить уведомления":
        await session.execute(update(WB).where(WB.tg_user_id == message.from_user.id and WB.task == True).values(task=False))
        await session.commit()
        await message.answer(text="Все уведомления остановлены")
    elif message.text == "Получить информацию из БД":
        db_query = await session.execute(select(WB).order_by(WB.id.desc()).limit(5))
        text = f"|  id  |   tg_user_id  |   created_on  |   wb_id   |   task    |\n"
        for data in db_query.scalars():
            text += f"|{data.id}|{data.tg_user_id}|{data.created_on}|{data.wb_id}|{data.task}|\n"
        await message.answer(
            text="Данные из БД:\n{}".format(text)
        )


@router.message(WB_State.wb_id)
async def wb_show(message: Message, state: FSMContext, session: AsyncSession) -> None:
    await state.clear()
    wb_db = await session.merge(WB(tg_user_id=message.from_user.id, wb_id=message.text))
    await session.commit()
    wb_data = await wb_api(message.text)
    builder = InlineKeyboardBuilder().add(InlineKeyboardButton(text="Подписаться",
                                                               callback_data=WBCallback(wb="wb", id=wb_db.id).pack()))
    await message.answer(text=f'Название: {wb_data["name"]}\n'
                              f'Артикул: {wb_data["id"]}\n'
                              f'Цена: {int(wb_data["salePriceU"])/100}руб\n'
                              f'Рейтинг товара: {wb_data["supplierRating"]}\n'
                              f'Количество товара: {wb_data["stocks"]}\n',
                         reply_markup=builder.as_markup()
                         )


@router.callback_query(WBCallback.filter(F.wb == "wb"))
async def wb_sub(query: CallbackQuery, callback_data: WBCallback, session: AsyncSession) -> None:
    await session.execute(update(WB).where(WB.id == callback_data.id).values(task=True))
    await session.commit()
    await query.answer(text=f"Подписаны на обновления")


def get_kb(items: list[str]) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    [kb.button(text=item) for item in items]
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)
