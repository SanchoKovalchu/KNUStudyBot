from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram import types, Dispatcher
from bot_create import cursor, connection
class FormLogin(StatesGroup):
    login = State()  # Will be represented in storage as 'Form:login'
    password = State()  # Will be represented in storage as 'Form:password'


async def login_command(message: types.Message):
    # Set state
    await FormLogin.login.set()
    await message.reply("Твій логін?")


async def load_login(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['login'] = message.text

    await FormLogin.next()
    await message.reply("Твій пароль?")


async def load_password(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['password'] = message.text
        login = data['login']
        password = data['password']
        await state.finish()
        sql = "SELECT * FROM MySQLTestForBot WHERE user_login = %s"
        cursor.execute(sql, login)
        #
        for row in cursor:
            user_password = row["user_password"]
            user_PIB = row["user_PIB"]
            user_course = row["user_course"]
            user_group = row["user_group"]
        if user_password == password:
            await message.answer("Ви успішно ввійшли")
            await message.answer("Вітаємо!\n"
                                 "Ваші дані: \n"
                                 "ПІБ: " + user_PIB + "\n"
                                 "Курс: " + str(user_course) + "\n"
                                 "Група: " + user_group)
        else:
            await message.answer("Пароль неправильний")
        connection.commit()


def register_handlers_login(dp: Dispatcher):
    # dp.register_message_handler(login_command, commands='login')
    dp.register_message_handler(login_command, lambda message: message.text == "Вхід")
    dp.register_message_handler(load_login, state=FormLogin.login)
    dp.register_message_handler(load_password, state=FormLogin.password)