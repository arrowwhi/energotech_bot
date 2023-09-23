from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging

from config import TOKEN
import database as db
from getBot import get_bot

import bot_body as b
import dialogue as d

dp = Dispatcher(get_bot(), storage=MemoryStorage())

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    b.start_inline_register_handlers(dp)
    d.inline_register_handlers_dialogue(dp)
    b.inline_register_handlers(dp)
    print("Start")
    executor.start_polling(dp, skip_updates=True)
