from aiogram import types, Dispatcher
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

login_bt = KeyboardButton('Вхід')
register_bt = KeyboardButton('Реєстрація')
photo_bt = KeyboardButton('Фото')
delete_keyboard_bt = KeyboardButton('Видалити клавіатуру')

st_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

st_keyboard.add(login_bt, register_bt, photo_bt)
st_keyboard.add(delete_keyboard_bt)


async def delete_keyboard(message: types.Message):
    await message.reply("Видалено клавіатуру!", reply_markup=types.ReplyKeyboardRemove())


def register_handlers_keyboard(dp: Dispatcher):
    dp.register_message_handler(delete_keyboard, lambda message: message.text == "Видалити клавіатуру")