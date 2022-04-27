import logging
from aiogram import executor, types
from handlers import login
from handlers import register
from handlers import photo_loader
from bot_create import dp

photo_loader.register_handlers_files(dp)
login.register_handlers_login(dp)
register.register_handlers_register(dp)
logging.basicConfig(level=logging.INFO)


@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Вхід", "Реєстрація", "Фото"]
    delete_keyboard = ["Видалити клавіатуру"]
    keyboard.add(*buttons)
    keyboard.add(*delete_keyboard)
    await message.answer("Ласкаво прошу до StudyBot!", reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == "Видалити клавіатуру")
async def delete_keyboard(message: types.Message):
    await message.reply("Шкода!", reply_markup=types.ReplyKeyboardRemove())


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

