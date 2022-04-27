from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import  State, StatesGroup

from aiogram import types, Dispatcher
# import bot_key
from bot_create import cursor, bot, connection

# bot = bot_key.getBot()


class FSMFiles(StatesGroup):
    photo = State()
    name = State()
    description = State()


async def cm_start(message : types.Message):
    await FSMFiles.photo.set()
    await bot.send_message(message.chat.id,"Загрузить фото")


async def load_photo(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await FSMFiles.next()
    await message.reply("Название фото")


async def name_photo(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMFiles.next()
    await message.reply("Опис фото")


async def description_photo(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
    async with state.proxy() as data:
        await message.reply(str(data))
        sql = "INSERT INTO 	file_storage (name, description, file_id) " \
              + " VALUES (%s, %s, %s) "
        # Выполнить sql и передать 3 параметра.
        file_id = data['photo']
        name = data['name']
        description = data['description']
        cursor.execute(sql, (name, description, file_id))
        connection.commit()
        await message.reply("ВСТАВЛЕНО!")
    await state.finish()


async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('Ok')


def register_handlers_files(dp : Dispatcher):
    dp.register_message_handler(cm_start, lambda message: message.text == "Фото", state=None)
    dp.register_message_handler(load_photo, content_types = 'photo', state=FSMFiles.photo)
    dp.register_message_handler(name_photo,  state=FSMFiles.name)
    dp.register_message_handler(description_photo, state=FSMFiles.description)
    dp.register_message_handler(cancel_handler, state="*",commands='stop')
    dp.register_message_handler(cancel_handler, Text(equals='stop', ignore_case=True), state="*")