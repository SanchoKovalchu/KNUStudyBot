import logging

import db_conn

import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor

logging.basicConfig(level=logging.INFO)

API_TOKEN = '5302840148:AAGtGfjfQZWbwRn0mqPrv_rEqRhK9XEiarg'

bot = Bot(token=API_TOKEN)

connection = db_conn.getConnection()
print ("Connect successful!")

# For example use simple MemoryStorage for Dispatcher.
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
cursor = connection.cursor()


# States
class Form(StatesGroup):
    login = State()  # Will be represented in storage as 'Form:login'
    password = State()  # Will be represented in storage as 'Form:password'
    PIB = State()  # Will be represented in storage as 'Form:PIB'
    course = State()  # Will be represented in storage as 'Form:course'
    group = State()  # Will be represented in storage as 'Form:course'


@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    # Set state
    await Form.login.set()

    await message.reply("Твій логін?")


# You can use state '*' if you need to handle all states
@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Cancelling state %r', current_state)
    # Cancel state and inform user about it
    await state.finish()
    # And remove keyboard (just in case)
    await message.reply('Cancelled.', reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=Form.login)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['login'] = message.text

    await Form.next()
    await message.reply("Твій пароль?")

@dp.message_handler(state=Form.password)
async def process_age(message: types.Message, state: FSMContext):
    # Update state and data
    async with state.proxy() as data:
        data['password'] = message.text
    await Form.next()
    await message.reply("Твоє ПІБ?")


@dp.message_handler(state=Form.PIB)
async def process_age(message: types.Message, state: FSMContext):
    # Update state and data
    async with state.proxy() as data:
        data['PIB'] = message.text
    await Form.next()
    # Configure ReplyKeyboardMarkup
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("1", "2", "3", "4")

    await message.answer("Твій курс?", reply_markup=markup)


@dp.message_handler(lambda message: message.text not in ["1", "2", "3", "4"], state=Form.course)
async def process_gender_invalid(message: types.Message):
    return await message.reply("Помилка. Оберіть курс із клавіатури")


@dp.message_handler(state=Form.course)
async def process_gender(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['course'] = message.text
        await Form.next()

        # Configure ReplyKeyboardMarkup
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        markup.add("IPZ-#1", "IPZ-#2", "IPZ-#3", "IPZ-#4")

        await message.answer("Твоя група?", reply_markup=markup)


@dp.message_handler(lambda message: message.text not in ["IPZ-#1", "IPZ-#2", "IPZ-#3", "IPZ-#4"], state=Form.group)
async def process_gender_invalid(message: types.Message):
    return await message.reply("Помилка. Виберіть групу із клавіатури.")


@dp.message_handler(state=Form.group)
async def process_age(message: types.Message, state: FSMContext):
    # Update state and data
    async with state.proxy() as data:
        data['group'] = message.text

        user_login = data['login']
        user_password = data['password']
        user_PIB = data['PIB']
        user_course = data['course']
        user_group = data['group']

        markup = types.ReplyKeyboardRemove()
        await bot.send_message(
            message.chat.id,
            md.text(
                md.text('Логін', md.bold(data['login'])),
                md.text('Пароль:', md.code(data['password'])),
                md.text('ПІБ:', data['PIB']),
                md.text('Курс:', data['course']),
                md.text('Група:', data['group']),
                sep='\n',
            ),
            reply_markup=markup,
            parse_mode=ParseMode.MARKDOWN,
        )
    await state.finish()

    sql = "INSERT INTO MySQLTestForBot (user_id, user_login, user_password, user_PIB, user_course, user_group) " \
          + " VALUES (%s, %s, %s, %s, %s, %s) "
    user_id = message.from_user.id
    cursor.execute(sql, (user_id, user_login, user_password, user_PIB, user_course, user_group))
    connection.commit()
    await message.answer("Зареєстровано!\nВаше ім'я:\t" + user_login + "\nВаше Прізвище: " + user_password)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)