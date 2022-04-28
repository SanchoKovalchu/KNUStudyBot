from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from bot_create import cursor, bot
from aiogram import types, Dispatcher
from keyboard.discipline_keyboard import dsp_keyboard, list
from keyboard.teacher_keyboard import tch_keyboard

class FSMViewFiles(StatesGroup):
    discipline = State()

async def cm_start(message: types.Message):
    await FSMViewFiles.discipline.set()
    await bot.send_message(message.chat.id, "Виберіть дисципліну, файли якої хочете побачити", reply_markup=dsp_keyboard)

async def mistake_discipline(message: types.Message):
    return await message.reply("Помилка. Оберіть дисципліну з клавіатури")

async def sql_read_file(message: types.message, state: FSMContext):
    await message.reply(f'Усі файли з дисципліни "{message.text}": ', reply_markup=tch_keyboard)
    sql = "SELECT * FROM file_storage WHERE subject = %s"
    cursor.execute(sql, message.text)
    for row in cursor.fetchall():
        if row["file_type"] == 'photo':
            await bot.send_photo(message.chat.id, row["file_id"], caption=  f'Назва: {row["name"]}\nОпис: {row["description"]}')
        elif row["file_type"] == 'video':
            await bot.send_video(message.chat.id, row["file_id"], caption= f'Назва: {row["name"]}\nОпис: {row["description"]}')
        elif row["file_type"] == 'audio':
            await bot.send_audio(message.chat.id, row["file_id"], caption=  f'Назва: {row["name"]}\nОпис: {row["description"]}')
        elif row["file_type"] == 'voice':
            await bot.send_voice(message.chat.id, row["file_id"], caption=  f'Назва: {row["name"]}\nОпис: {row["description"]}')
        elif row["file_type"] == 'animation':
            await bot.send_animation(message.chat.id, row["file_id"], caption=  f'Назва: {row["name"]}\nОпис: {row["description"]}')
        elif row["file_type"] == 'video_note':
            await bot.send_video_note(message.chat.id, row["file_id"], caption=  f'Назва: {row["name"]}\nОпис: {row["description"]}')
        else:
            await bot.send_document(message.chat.id, row["file_id"], caption=  f'Назва: {row["name"]}\nОпис: {row["description"]}')
    await state.finish()

def register_handlers_files(dp : Dispatcher):
    dp.register_message_handler(cm_start, lambda message: message.text == "Переглянути матеріал", state=None)
    dp.register_message_handler(mistake_discipline, lambda message: message.text not in list, state=FSMViewFiles.discipline)
    dp.register_message_handler(sql_read_file, state=FSMViewFiles.discipline)