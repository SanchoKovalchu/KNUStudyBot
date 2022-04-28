from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

login_bt = KeyboardButton('Вхід')
register_bt = KeyboardButton('Реєстрація')

first_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

first_keyboard.add(login_bt, register_bt)
