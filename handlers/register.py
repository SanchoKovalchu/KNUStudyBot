from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import logging
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from bot_create import cursor, connection
from keyboard import first_keyboard


class FormRegister(StatesGroup):
    login = State()  # Will be represented in storage as 'Form:login'
    password = State()  # Will be represented in storage as 'Form:password'
    PIB = State()  # Will be represented in storage as 'Form:PIB'
    sp = State()  # Will be represented in storage as 'Form:sp'
    course = State()  # Will be represented in storage as 'Form:course'
    group = State()  # Will be represented in storage as 'Form:group'


async def register_command(message: types.Message):
    # Set state
    await FormRegister.login.set()
    await message.reply("Твій логін?")


async def cancel_command(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    logging.info('Cancelling state %r', current_state)
    await state.finish()
    await message.reply('Cancelled.', reply_markup=types.ReplyKeyboardRemove())


async def load_login(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['login'] = message.text

    await FormRegister.next()
    await message.reply("Твій пароль?")


async def load_password(message: types.Message, state: FSMContext):
    # Update state and data
    async with state.proxy() as data:
        data['password'] = message.text
    await FormRegister.next()
    await message.reply("Твоє ПІБ?")


async def load_PIB(message: types.Message, state: FSMContext):
    # Update state and data
    async with state.proxy() as data:
        data['PIB'] = message.text
    await FormRegister.next()
    # Configure ReplyKeyboardMarkup
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("IPZ", "PP", "AND", "KN")

    await message.answer("Твоя навчальна програма?", reply_markup=markup)


async def mistake_sp(message: types.Message):
    return await message.reply("Помилка. Оберіть навчальну програму із клавіатури")


async def load_sp(message: types.Message, state: FSMContext):
    # Update state and data
    async with state.proxy() as data:
        data['sp'] = message.text
    await FormRegister.next()
    # Configure ReplyKeyboardMarkup
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("1", "2", "3", "4", "5", "6")

    await message.answer("Твій курс?", reply_markup=markup)


async def mistake_course(message: types.Message):
    return await message.reply("Помилка. Оберіть курс із клавіатури")


async def load_course(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['course'] = message.text
        await FormRegister.next()
        # Configure ReplyKeyboardMarkup
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        markup.add("1", "2", "3", "4", "5")

        await message.answer("Твоя група?", reply_markup=markup)


async def mistake_group(message: types.Message):
    return await message.reply("Помилка. Виберіть групу із клавіатури.")


async def load_group(message: types.Message, state: FSMContext):
    # Update state and data
    async with state.proxy() as data:
        data['group'] = message.text
        user_login = data['login']
        user_password = data['password']
        user_PIB = data['PIB']
        user_sp = data['sp']
        user_course = data['course']
        user_group = data['group']
    await state.finish()

    sql = "INSERT INTO MySQLTestForBot (user_id, user_login, user_password, user_PIB, user_sp, user_course, user_group) " \
          + " VALUES (%s, %s, %s, %s, %s, %s, %s) "
    user_id = message.from_user.id
    cursor.execute(sql, (user_id, user_login, user_password, user_PIB, user_sp,user_course, user_group))

    connection.commit()
    await message.answer("Зареєстровано!\n"
                         "Ваші дані: \n"
                         "Логін: " + user_login + "\n"
                         "Пароль: " + user_password + "\n"
                         "ПІБ: " + user_PIB + "\n"
                         "Навчальна програма: " + user_sp + "\n"
                         "Курс: " + user_course + "\n"
                         "Група: " + user_group,
                         reply_markup=first_keyboard)


def register_handlers_register(dp: Dispatcher):
    dp.register_message_handler(register_command, lambda message: message.text == "Реєстрація")
    dp.register_message_handler(cancel_command, Text(equals='cancel', ignore_case=True), state='*')
    dp.register_message_handler(load_login, state=FormRegister.login)
    dp.register_message_handler(load_password, state=FormRegister.password)
    dp.register_message_handler(load_PIB, state=FormRegister.PIB)
    dp.register_message_handler(mistake_sp, lambda message: message.text not in ["IPZ", "PP", "AND", "KN"], state=FormRegister.sp)
    dp.register_message_handler(load_sp, state=FormRegister.sp)
    dp.register_message_handler(mistake_course, lambda message: message.text not in ["1", "2", "3", "4", "5", "6"], state=FormRegister.course)
    dp.register_message_handler(load_course, state=FormRegister.course)
    dp.register_message_handler(mistake_group, lambda message: message.text not in ["1", "2", "3", "4", "5"], state=FormRegister.group)
    dp.register_message_handler(load_group, state=FormRegister.group)