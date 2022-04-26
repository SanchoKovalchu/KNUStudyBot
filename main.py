import logging
import db_conn



from random import randint
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text, state

connection = db_conn.getConnection()
print ("Connect successful!")

bot = Bot(token="5302840148:AAGtGfjfQZWbwRn0mqPrv_rEqRhK9XEiarg")
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)
cursor = connection.cursor()


@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Вхід", "Реєстрація"]
    delete_keyboard = ["Видалити клавіатуру"]
    keyboard.add(*buttons)
    keyboard.add(*delete_keyboard)
    await message.answer("Ласкаво прошу до StudyBot!", reply_markup=keyboard)


@dp.message_handler(commands="special_buttons")
async def cmd_special_buttons(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text="Запросить геолокацию", request_location=True))
    keyboard.add(types.KeyboardButton(text="Запросить контакт", request_contact=True))
    keyboard.add(types.KeyboardButton(text="Создать викторину",
                                      request_poll=types.KeyboardButtonPollType(type=types.PollType.QUIZ)))
    await message.answer("Выберите действие:", reply_markup=keyboard)


@dp.message_handler(Text(equals="Вхід"))
async def login(message: types.Message):
    await message.reply("Отличный выбор!")
    user_id = message.from_user.id
    sql = "SELECT * FROM MySQLTestForBot WHERE user_id = %s"
    #Выполнить sql и передать 1 параметр.
    cursor.execute(sql, user_id)
    for row in cursor:
        await message.reply("Ваше ім'я:\t" + str(row["first_name"]) + "\nВаше Прізвище: " + row["last_name"])


@dp.message_handler(lambda message: message.text == "Реєстрація")
async def registration(message: types.Message):
    await message.reply("Так невкусно!")
    sql = "INSERT INTO MySQLTestForBot (user_id, first_name, last_name) " \
          + " VALUES (%s, %s, %s) "
    # Выполнить sql и передать 3 параметра.
    first_name = "Sancho"
    last_name = "Kovalchuk"
    user_id = message.from_user.id
    cursor.execute(sql, (user_id, first_name, last_name))
    connection.commit()
    await message.reply("ВСТАВЛЕНО!\nВаше ім'я:\t" + first_name + "\nВаше Прізвище: " + last_name)


@dp.message_handler(lambda message: message.text == "Видалити клавіатуру")
async def delete_keyboard(message: types.Message):
    await message.reply("Шкода!", reply_markup=types.ReplyKeyboardRemove())

# @dp.message_handler()
# async def any_text_message(message: types.Message):
#     await message.answer(message.text)
#     await message.answer(message.md_text)
#     await message.answer(message.html_text)
#     # Дополняем исходный текст:
#     await message.answer(
#         f"<u>Ваш текст</u>:\n\n{message.html_text}", parse_mode="HTML"
#     )


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)




# import logging
# from random import randint
#
# from aiogram import Bot, Dispatcher, executor, types
# from aiogram.dispatcher.filters import Text
#
# bot = Bot(token="5302840148:AAGtGfjfQZWbwRn0mqPrv_rEqRhK9XEiarg")
# dp = Dispatcher(bot)
# logging.basicConfig(level=logging.INFO)
#
# @dp.message_handler(commands="start")
# async def cmd_start(message: types.Message):
#     keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     buttons = ["Вхід", "Реєстрація", "Рандом"]
#     delete_keyboard = ["Видалити клавіатуру"]
#     keyboard.add(*buttons)
#     keyboard.add(*delete_keyboard)
#     await message.answer("Ласкаво прошу до StudyBot!", reply_markup=keyboard)
#
#
# @dp.message_handler(Text(equals="Вхід"))
# async def login(message: types.Message):
#     await message.reply("Отличный выбор!")
#
#
# @dp.message_handler(lambda message: message.text == "Реєстрація")
# async def registration(message: types.Message):
#     await message.reply("Так невкусно!")\
#
#
# @dp.message_handler(lambda message: message.text == "Рандом")
# async def random(message: types.Message):
#     keyboard = types.InlineKeyboardMarkup()
#     keyboard.add(types.InlineKeyboardButton(text="Нажми меня", callback_data="random_value"))
#     await message.answer("Нажмите на кнопку, чтобы бот отправил число от 1 до 10", reply_markup=keyboard)
#
#
# @dp.callback_query_handler(text="random_value")
# async def send_random_value(call: types.CallbackQuery):
#     await call.message.answer(str(randint(1, 10)))
#
#
# @dp.message_handler(lambda message: message.text == "Видалити клавіатуру")
# async def delete_keyboard(message: types.Message):
#     await message.reply("Шкода!", reply_markup=types.ReplyKeyboardRemove())
#
#
# if __name__ == "__main__":
#     executor.start_polling(dp, skip_updates=True)