import schedule
import time
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram import types, Dispatcher
from bot_create import cursor
from bot_create import bot
from handlers.login import UserRoles
from keyboard import tch_keyboard

class FormAnnounce(StatesGroup):
    receivers1 = State()
    receivers2 = State()
    course = State()
    sp = State()
    group = State()
    person = State()
    cathedra = State()
    text = State()
    havefile = State()
    file = State()
    content = State()
    confirmation = State()


async def announcement_command(message: types.Message):
    # Set state

    await FormAnnounce.receivers1.set()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("Студент(-и)", "Викладач(-і)")
    await message.reply("Хто має отримати повідомлення?", reply_markup=markup)

async def mistake_receivers1(message: types.Message):
    return await message.reply("Помилка. Оберіть отримувачів з клавіатури")

async def load_receivers1(message: types.Message):
    # Set state
    await FormAnnounce.receivers2.set()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    if(message.text == 'Студент(-и)'):
        markup.add("Курс", "Спеціальність", "Група", "Студент")
    elif (message.text == 'Викладач(-і)'):
        markup.add("Усі викладачі кафедри", "Один викладач")
    await message.reply("Вкажіть вибірку отримувачів", reply_markup=markup)

async def mistake_receivers2(message: types.Message):
    return await message.reply("Помилка. Оберіть отримувачів з клавіатури")

async def load_receivers2(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['receivers'] = message.text
        user_receivers = data['receivers']
    if user_receivers == 'Один викладач':
        await FormAnnounce.person.set()
        await message.reply("Введіть ПІБ викладача:")
    elif user_receivers == 'Усі викладачі кафедри':
        await FormAnnounce.cathedra.set()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        markup.add("IPZ", "PP", "AND", "KN")
        await message.reply("Яка кафедра?", reply_markup=markup)
    elif user_receivers == 'Студент':
        await FormAnnounce.person.set()
        await message.reply("Введіть ПІБ студента:")
    else:
        await FormAnnounce.next()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        markup.add("1", "2", "3", "4", "5", "6")
        await message.reply("Який курс?", reply_markup=markup)

async def mistake_cathedra(message: types.Message):
    return await message.reply("Помилка. Оберіть курс із клавіатури")

async def load_cathedra(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['cathedra'] = message.text
    await FormAnnounce.havefile.set()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("Так", "Ні")
    await message.reply("Додати файл?", reply_markup=markup)


async def mistake_course(message: types.Message):
    return await message.reply("Помилка. Оберіть курс із клавіатури")

async def load_course(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['course'] = message.text
        user_receivers = data['receivers']
    if  user_receivers != 'Курс':
        await FormAnnounce.next()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        markup.add("IPZ", "PP", "AND", "KN")
        await message.reply("Яка спеціальність?", reply_markup=markup)
    else:
        await FormAnnounce.havefile.set()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        markup.add("Так", "Ні")
        await message.reply("Додати файл?", reply_markup=markup)

async def mistake_sp(message: types.Message):
    return await message.reply("Помилка. Оберіть спеціальність із клавіатури")

async def load_sp(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['sp'] = message.text
        user_receivers = data['receivers']
    if  user_receivers != 'Спеціальність':
        await FormAnnounce.next()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        markup.add("1", "2", "3", "4", "5")
        await message.reply("Яка група?", reply_markup=markup)
    else:
        await FormAnnounce.havefile.set()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        markup.add("Так", "Ні")
        await message.reply("Додати файл?", reply_markup=markup)

async def mistake_group(message: types.Message):
    return await message.reply("Помилка. Оберіть групу із клавіатури")

async def load_group(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['group'] = message.text
    await FormAnnounce.havefile.set()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("Так", "Ні")
    await message.reply("Додати файл?", reply_markup=markup)

async def load_PIB(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['PIB'] = message.text
    await FormAnnounce.havefile.set()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("Так", "Ні")
    await message.reply("Додати файл?", reply_markup=markup)

async def mistake_havefile(message: types.Message):
    return await message.reply("Помилка. Оберіть відповідь із клавіатури")

async def load_havefile (message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['havefile'] = message.text
    if message.text=='Так':
        await FormAnnounce.file.set()
        await bot.send_message(message.chat.id, "Відправте файл", reply_markup=types.ReplyKeyboardRemove())
    else:
        await FormAnnounce.content.set()
        await bot.send_message(message.chat.id, "Введіть текст повідомлення", reply_markup=types.ReplyKeyboardRemove())

async def load_file (message: types.Message, state: FSMContext):
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
    await FormAnnounce.content.set()
    await bot.send_message(message.chat.id, "Введіть текст повідомлення", reply_markup=types.ReplyKeyboardRemove())


# async def load_text (message: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         data['text'] = message.text
#



async def load_content(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text
        user_havefile = data['havefile']
        user_receivers = data['receivers']
        if user_receivers == 'Курс' or user_receivers == 'Спеціальність' or user_receivers == 'Група':
            user_course = data['course']
        if user_receivers == 'Спеціальність' or user_receivers == 'Група':
            user_sp = data['sp']
        if user_receivers == 'Група':
            user_group = data['group']
        if user_receivers == 'Студент' or user_receivers == 'Один викладач':
            user_PIB = data['PIB']
        if user_receivers == 'Усі викладачі кафедри':
            user_cathedra = data['cathedra']
        if user_havefile == 'Так':
            user_file_type = data['type']
            user_file_id = data['file_id']
        user_text = data['text']
    if user_receivers == 'Курс':
        await message.answer("Таке повідомлення буде надіслано студентам "+user_course+"-ого курсу:")
    elif user_receivers == 'Спеціальність':
        await message.answer("Таке повідомлення буде надіслано студентам "+user_course+"-ого курсу спеціальності "+user_sp+":")
    elif user_receivers == 'Група':
        await message.answer("Таке повідомлення буде надіслано студентам групи" + user_sp + "-" + user_course+user_group+":")
    elif user_receivers == 'Студент':
        await message.answer("Таке повідомлення буде надіслано студенту, ПІБ якого " + user_PIB+":")
    elif user_receivers == 'Один викладач':
        await message.answer("Таке повідомлення буде надіслано викладачу, ПІБ якого " + user_PIB + ":")
    elif user_receivers == 'Усі викладачі кафедри':
        await message.answer("Таке повідомлення буде надіслано викладачам кафедри " + user_cathedra + ":")
    if user_havefile == 'Ні':
        await message.answer(user_text)
    else:
        match user_file_type:
            case 'photo':
                await bot.send_photo(message.chat.id, user_file_id, caption=user_text)
            case 'video':
                await bot.send_video(message.chat.id, user_file_id, caption=user_text)
            case 'audio':
                await bot.send_audio(message.chat.id, user_file_id, caption=user_text)
            case 'voice':
                await bot.send_voice(message.chat.id, user_file_id, caption=user_text)
            case 'animation':
                await bot.send_animation(message.chat.id, user_file_id, caption=user_text)
            case 'video_note':
                await bot.send_video_note(message.chat.id, user_file_id, caption=user_text)
            case _:
                await bot.send_document(message.chat.id, user_file_id, caption=user_text)
    await FormAnnounce.confirmation.set()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("Надіслати", "Відмінити")
    await message.reply("Надіслати повідомлення?", reply_markup=markup)

async def mistake_confirmation(message: types.Message):
    return await message.reply("Помилка. Оберіть відповідь із клавіатури")

async def load_confirmation(message: types.Message, state: FSMContext):
    if message.text == "Відмінити" :
        await message.answer("Відмінено відправку оголошення", reply_markup=types.ReplyKeyboardRemove())
        await state.finish()
        await UserRoles.teacher.set()
        return
    else:
        async with state.proxy() as data:
            user_havefile = data['havefile']
            user_receivers = data['receivers']
            if user_receivers == 'Курс' or user_receivers == 'Спеціальність' or user_receivers == 'Група':
                user_course = data['course']
            if user_receivers == 'Спеціальність' or user_receivers == 'Група':
                user_sp = data['sp']
            if user_receivers == 'Група':
                user_group = data['group']
            if user_receivers == 'Студент' or user_receivers == 'Один викладач':
                user_PIB = data['PIB']
            if user_receivers == 'Усі викладачі кафедри':
                user_cathedra = data['cathedra']
            if user_havefile == 'Так':
                user_file_type = data['type']
                user_file_id = data['file_id']
            user_text = data['text']
        await state.finish()
        await UserRoles.teacher.set()
        if user_receivers=='Курс':
            sql = "SELECT * FROM student_data WHERE course = %s"
            cursor.execute(sql, user_course)
            rec = cursor.fetchall()
        elif user_receivers=='Спеціальність':
            sql = "SELECT * FROM student_data WHERE course = %s AND sp = %s"
            cursor.execute(sql, (user_course, user_sp))
            rec = cursor.fetchall()
        elif user_receivers=='Група':
            sql = "SELECT * FROM student_data WHERE course = %s AND sp = %s AND st_group = %s"
            cursor.execute(sql, (user_course, user_sp, user_group))
            rec = cursor.fetchall()
        elif user_receivers=='Студент':
            sql = "SELECT * FROM student_data WHERE PIB = %s"
            cursor.execute(sql, user_PIB)
            rec = cursor.fetchall()
        elif user_receivers=='Один викладач':
            sql = "SELECT * FROM teacher_data WHERE PIB = %s"
            cursor.execute(sql, user_PIB)
            rec = cursor.fetchall()
        else :
            sql = "SELECT * FROM teacher_data WHERE cathedra = %s"
            cursor.execute(sql, user_cathedra)
            rec = cursor.fetchall()
        for row in rec:
            if user_havefile == 'Ні':
                await bot.send_message(row['user_id'], user_text)
            else:
                match user_file_type:
                    case 'photo':
                        await bot.send_photo(row['user_id'], user_file_id, caption=user_text)
                    case 'video':
                        await bot.send_video(row['user_id'], user_file_id, caption=user_text)
                    case 'audio':
                        await bot.send_audio(row['user_id'], user_file_id, caption=user_text)
                    case 'voice':
                        await bot.send_voice(row['user_id'], user_file_id, caption=user_text)
                    case 'animation':
                        await bot.send_animation(row['user_id'], user_file_id, caption=user_text)
                    case 'video_note':
                        await bot.send_video_note(row['user_id'], user_file_id, caption=user_text)
                    case _:
                        await bot.send_document(row['user_id'], user_file_id, caption=user_text)
        await message.answer("Оголошення надіслано успішно!",  reply_markup=tch_keyboard)

def register_handlers_announcement(dp: Dispatcher):
    dp.register_message_handler(announcement_command, lambda message: message.text == "Оголошення", state=UserRoles.teacher)
    dp.register_message_handler(mistake_receivers1, lambda message: message.text not in ["Студент(-и)", "Викладач(-і)"], state=FormAnnounce.receivers1)
    dp.register_message_handler(mistake_receivers2, lambda message: message.text not in ["Курс", "Спеціальність", "Група", "Студент","Усі викладачі кафедри", "Один викладач"], state=FormAnnounce.receivers2)
    dp.register_message_handler(load_receivers1, state=FormAnnounce.receivers1)
    dp.register_message_handler(load_receivers2, state=FormAnnounce.receivers2)
    dp.register_message_handler(mistake_cathedra, lambda message: message.text not in ["IPZ", "PP", "AND", "KN"],state=FormAnnounce.cathedra)
    dp.register_message_handler(load_cathedra, state=FormAnnounce.cathedra)
    dp.register_message_handler(mistake_course,lambda message: message.text not in ["1", "2", "3", "4", "5", "6"],state=FormAnnounce.course)
    dp.register_message_handler(load_course, state=FormAnnounce.course)
    dp.register_message_handler(mistake_sp, lambda message: message.text not in ["IPZ", "PP", "AND", "KN"],state=FormAnnounce.sp)
    dp.register_message_handler(load_sp, state=FormAnnounce.sp)
    dp.register_message_handler(mistake_group, lambda message: message.text not in ["1", "2", "3", "4", "5"],state=FormAnnounce.group)
    dp.register_message_handler(load_group, state=FormAnnounce.group)
    dp.register_message_handler(load_PIB, state=FormAnnounce.person)
    dp.register_message_handler(mistake_havefile, lambda message: message.text not in ["Так", "Ні"], state=FormAnnounce.havefile)
    dp.register_message_handler(load_havefile, state=FormAnnounce.havefile)
    dp.register_message_handler(load_file,content_types = ['photo','video','audio','document','animation','video_note','voice'], state=FormAnnounce.file)
    dp.register_message_handler(load_content, state=FormAnnounce.content)
    dp.register_message_handler(mistake_confirmation, lambda message: message.text not in ["Надіслати", "Відмінити"], state=FormAnnounce.confirmation)
    dp.register_message_handler(load_confirmation, state=FormAnnounce.confirmation)