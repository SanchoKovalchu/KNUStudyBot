from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram import types, Dispatcher
from handlers.login import UserRoles
from keyboard.teacher_keyboard import tch_keyboard
from aiogram.dispatcher.filters import Text
from bot_create import connection, cursor, bot
from datetime import datetime


async def view_polls(message: types.Message):
    sql = "SELECT * FROM poll_storage"
    cursor.execute(sql)
    chat_id = []
    message_id = []
    date_time = []

    i = -1
    for row in cursor:
        i += 1
        chat_id.append(row["chat_id"])
        message_id.append(row["message_id"])
        date_time.append(row["datetime"])
    n = -1
    for i in range(len(chat_id)):
        await bot.forward_message(message.from_user.id, chat_id[i], message_id[i])
        n += 2
        if i == 0:
            await bot.send_message(message.from_user.id, "Дата опитування: " + date_time[i], reply_markup=tch_keyboard, reply_to_message_id=message.message_id+1)
        else:
            await bot.send_message(message.from_user.id, "Дата опитування: " + date_time[i], reply_markup=tch_keyboard, reply_to_message_id=message.message_id+n)

    if len(chat_id) == 0:
        await bot.send_message(message.chat.id, "Опитування відсутні", reply_markup=tch_keyboard)

async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await UserRoles.teacher.set()
    await message.reply('Ok', reply_markup=tch_keyboard)


def register_handlers_poll_view(dp: Dispatcher):
    dp.register_message_handler(view_polls, lambda message: message.text == "Переглянути опитування", state=UserRoles.teacher)
    dp.register_message_handler(cancel_handler, state="*", commands='stop')
    dp.register_message_handler(cancel_handler, Text(equals='stop', ignore_case=True), state="*")