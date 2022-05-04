from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import  State, StatesGroup
from keyboard.teacher_keyboard import tch_keyboard
from keyboard.discipline_keyboard import dsp_keyboard, list
#from keyboard.addmaterial_keyboard import am_keyboard  # Додаткове
from aiogram import types, Dispatcher
# import bot_key
from bot_create import cursor, bot, connection



class FSMFiles(StatesGroup):
    discipline_ = State()
    document_ = State()
    name_ = State()
    description_ = State()
    send_date_ = State()


async def cm_start_(message : types.Message):
    await FSMFiles.discipline_.set()
    await bot.send_message(message.chat.id, "Виберіть дисципліну, до якої хочете завантажити додатковий файл", reply_markup=dsp_keyboard)

async def mistake_disciplines_(message: types.Message):
    return await message.reply("Помилка. Оберіть дисципліну з клавіатури")

async def choose_discipline_(message : types.message, state: FSMContext):
    async with state.proxy() as data:
        data['subject'] = message.text
    await FSMFiles.next()
    await bot.send_message(message.chat.id, "Відправте файл")


async def upload_file_(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['type'] = message.content_type
        if data['type'] == 'photo':
            data['file_id'] = message.photo[0].file_id
        elif data['type'] == 'video':
            data['file_id'] = message.video.file_id
        elif data['type'] == 'voice':
            data['file_id'] = message.voice.file_id
        elif data['type'] == 'audio':
            data['file_id'] = message.audio.file_id
        elif data['type'] == 'animation':
            data['file_id'] = message.animation.file_id
        elif data['type'] == 'video_note':
            data['file_id'] = message.video_note.file_id
        else:
            data['file_id'] = message.document.file_id
    await FSMFiles.next()
    await message.reply("Яка назва файлу?")


async def file_name_(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text


    await FSMFiles.next()
    await message.reply("Опишіть вміст файлу")


async def file_description_(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text


        await FSMFiles.next()
        await message.reply("Введіть дату та час відправлення.\n Приклад: 2022-01-20 08:03:20")


async def file_send_date_(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['send_date'] = message.text

    async with state.proxy() as data:
        sql = "INSERT INTO 	add_file_storage (name, description, file_id, file_type, subject, send_date) " \
              + " VALUES (%s, %s, %s, %s, %s, %s) "
        # Выполнить sql и передать 3 параметра.
        subject = data['subject']
        file_type = data['type']
        file_id = data['file_id']
        name = data['name']
        description = data['description']
        send_date = data['send_date']
        cursor.execute(sql, (name, description, file_id, file_type, subject, send_date))
        connection.commit()
        await message.reply("Заплановано!", reply_markup=tch_keyboard)
        await state.finish()


async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('Ok', reply_markup=tch_keyboard)

def register_handlers_files(dp : Dispatcher):
    dp.register_message_handler(cm_start_, lambda message: message.text == "Додати додатковий матеріал", state=None)
    dp.register_message_handler(mistake_disciplines_, lambda message: message.text not in list, state=FSMFiles.discipline_)
    dp.register_message_handler(choose_discipline_, state=FSMFiles.discipline_)
    dp.register_message_handler(upload_file_,content_types = ['photo','video','audio','document','animation','video_note','voice'], state=FSMFiles.document_)
    dp.register_message_handler(file_name_,  state=FSMFiles.name_)
    dp.register_message_handler(file_description_, state=FSMFiles.description_)
    dp.register_message_handler(file_send_date_, state=FSMFiles.send_date_)
    dp.register_message_handler(cancel_handler, state="*",commands='stop')
    dp.register_message_handler(cancel_handler, Text(equals='stop', ignore_case=True), state="*")