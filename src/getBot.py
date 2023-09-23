from aiogram import Bot

from config import TOKEN

bot = Bot(token=TOKEN)


def get_bot():
    return bot
