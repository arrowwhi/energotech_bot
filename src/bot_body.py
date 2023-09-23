import logging
import sqlite3

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import (
    KeyboardButton, ReplyKeyboardMarkup,
)

import config as config
# from aiogram.utils.callback_data import CallbackData
# from aiogram.utils.exceptions import BotBlocked
# from config import TOKEN, admin_id
# from aiogram.contrib.fsm_storage.memory import MemoryStorage

from getBot import get_bot

# import database as db
import messages as mg
import chat_gpt_body as gpt


class ChatState(StatesGroup):
    on_dialogue = State()
    back_call = State()
    default = State()
    get_chat = State()
    wait_question = State()


async def get_back_call_info(message: types.Message, state: FSMContext):
    await ChatState.back_call.set()
    await message.answer("Пожалуйста, напишите ваше имя, контактные данные \
и удобное время для звонка в ответ на это сообщение")


async def take_back_order(message: types.Message, state: FSMContext):
    to_support_msg = f"Заявка на обратный звонок от {message.from_user.first_name} {message.from_user.last_name}: \n" \
                     + message.text

    q = await get_bot().send_message(chat_id=config.group_id, text=to_support_msg)
    print(q)
    await state.finish()
    await message.answer('Успешно отправлено!', reply_markup=mg.get_main_keyboard())


def get_cancel_keyboard():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    b1 = KeyboardButton("Отменить")
    kb.add(b1)
    return kb


def stop_talk_keyboard():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    b1 = KeyboardButton("Прекратить диалог")
    kb.add(b1)
    return kb


async def press_start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(mg.start_message, reply_markup=mg.get_main_keyboard())


async def default_start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(mg.end_dialog, reply_markup=mg.get_main_keyboard())


async def press_about(message: types.Message, state: FSMContext):
    await message.answer(mg.about_message, reply_markup=mg.get_main_keyboard())


async def start_talk(message: types.Message, state: FSMContext):
    await ChatState.get_chat.set()
    await message.answer(mg.start_talk, reply_markup=mg.get_chatbot_keyboard())


async def talk_with_bot(message: types.Message, state: FSMContext):
    if message.content_type != 'text':
        return
    result = await message.answer('Я думаю над ответом...')
    ans = gpt.openAI(message.from_user.id, message.text)
    await result.edit_text(ans)


async def get_presentation(message: types.Message, state: FSMContext):
    await get_bot().send_document(message.chat.id, document=config.catalog_id)


def start_inline_register_handlers(dp: Dispatcher):
    dp.register_message_handler(
        press_start, commands="start", state="*")
    dp.register_message_handler(
        press_start, text="Отменить", state="*")
    dp.register_message_handler(
        default_start, lambda message: message.text and message.text.startswith("Прекратить диалог"),
        state="*")


def inline_register_handlers(dp: Dispatcher):
    dp.register_message_handler(
        get_presentation, text="Получить презентацию", state="*")
    dp.register_message_handler(
        press_about, text="О наc", state="*")
    dp.register_message_handler(
        get_back_call_info, text="Заказать обратный звонок", state="*")
    dp.register_message_handler(
        start_talk, text="Написать в поддержку", state="*")
    dp.register_message_handler(
        talk_with_bot, state=ChatState.get_chat)
    dp.register_message_handler(
        take_back_order, state=ChatState.back_call)
