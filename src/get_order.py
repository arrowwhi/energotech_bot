from aiogram import  Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup,
                           ReplyKeyboardRemove)
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.exceptions import BotBlocked

import config as config
from config import TOKEN, admin_id
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from main import bot

from bot_body import OrderState
import messages as mg


async def start_talk(message: types.Message, state: FSMContext):
    await message.answer(mg.order_start, reply_markup=mg.order_start_kb())
    await OrderState.buy_type.set()


async def get_type(message: types.Message, state: FSMContext):
    if message.text not in mg.order_type_btns:
        await message.answer("Пожалуйста, выберите тип на клавиатуре")
        return
    await state.update_data(type=message.text)
    user_data = await state.get_data()
    print(user_data)
    await message.answer("Напишите габариты электрощита, который вам нужен")
    await OrderState.enter_size.set()


async def get_size(message: types.Message, state: FSMContext):
    await state.update_data(size=message.text)
    user_data = await state.get_data()
    print(user_data)
    await message.answer("Укажите, на какую стоимость вы рассчитываете")
    await OrderState.enter_price.set()


async def get_price(message: types.Message, state: FSMContext):
    await state.update_data(price=message.text)
    user_data = await state.get_data()
    print(user_data)
    await message.answer(mg.get_final_msg(user_data), reply_markup=mg.get_final_order_btns())
    await OrderState.final.set()


async def get_final(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    if message.text != 'Подтвердить':
        await state.update_data(comment=(str(user_data.get('comment', '') + '\n' + message.text)))
        user_data = await state.get_data()
        await message.answer(mg.get_final_msg(user_data))
        return
    await bot.send_message(config.admin_id, str(user_data)+message.chat.first_name+' ' + message.chat.last_name + ' ' +
                           message.chat.id)
    await message.answer('Успешно отправлено', reply_markup=mg.get_main_keyboard())
    await OrderState.next()


def inline_order_handlers(dp: Dispatcher):
    dp.register_message_handler(
        start_talk, text="Заказать оборудование", state="*")
    dp.register_message_handler(
        get_type, state=OrderState.buy_type)
    dp.register_message_handler(
        get_size, state=OrderState.enter_size)
    dp.register_message_handler(
        get_price, state=OrderState.enter_price)
    dp.register_message_handler(
        get_final, state=OrderState.final)




