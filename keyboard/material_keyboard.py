from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

add_material_bt = KeyboardButton('Додати матеріал')
add_additional_material_bt = KeyboardButton('Додати додатковий матеріал')
edit_material_bt = KeyboardButton('Редагувати матеріал')
delete_material_bt = KeyboardButton('Видалити матеріал')
view_material_bt = KeyboardButton('Переглянути матеріал')



mtrl_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

mtrl_keyboard.add(add_material_bt)
mtrl_keyboard.add(add_additional_material_bt)
mtrl_keyboard.add(edit_material_bt)
mtrl_keyboard.add(delete_material_bt)
mtrl_keyboard.add(view_material_bt)