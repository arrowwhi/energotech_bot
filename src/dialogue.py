from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
import config as config
from bot_body import ChatState
import messages as mg
from getBot import get_bot

start_dialogue_message = "Чат с менеджером открыт. Пожалуйста, напишите свой вопрос."


async def start_talk(message: types.Message, state: FSMContext):
    await ChatState.on_dialogue.set()
    await message.answer(start_dialogue_message, reply_markup=mg.get_chatbot_keyboard())


async def stop_talk(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Чат с менеджером закрыт.", reply_markup=mg.get_main_keyboard())


async def answer_to_client(message: types.Message, state: FSMContext):
    try:
        person = message.reply_to_message.text.split(' ')[-1]
    except Exception:
        await message.answer("Не удалось отправить сообщение.")
        return
    await get_bot().send_message(chat_id=person, text=message.text)
    return


async def transfer_message(message: types.Message, state: FSMContext):
    to_support_msg = f"Сообщение от пользователя {message.from_user.first_name} {message.from_user.last_name}: \n" \
                     + message.text + f"\n\n {message.from_user.id}"
    await get_bot().send_message(chat_id=config.group_id, text=to_support_msg)

    await message.answer("Сообщение передано! В скором времени с вами свяжется менеджер.")


def inline_register_handlers_dialogue(dp: Dispatcher):
    dp.register_message_handler(
        start_talk, text='Поговорить с менеджером', state=ChatState.get_chat)
    dp.register_message_handler(
        stop_talk, lambda message: message.text and message.text.startswith("Прекратить диалог"),
        state=ChatState.on_dialogue)
    dp.register_message_handler(
        answer_to_client, chat_type=[types.ChatType.SUPERGROUP], is_reply=True)
    dp.register_message_handler(
        transfer_message, state=ChatState.on_dialogue)
