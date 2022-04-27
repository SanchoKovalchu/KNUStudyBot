from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
disciplines_bt = KeyboardButton('Перелік дисциплін')
groups_bt = KeyboardButton('Групи студентів')
material_bt = KeyboardButton('Матеріал')
tests_bt = KeyboardButton('Тести')
settings_bt = KeyboardButton('Налаштування')
# photo_bt = KeyboardButton('Фото')


tch_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

tch_keyboard.add(disciplines_bt)
tch_keyboard.add(groups_bt)
tch_keyboard.add(material_bt)
tch_keyboard.add(tests_bt)
tch_keyboard.add(settings_bt)