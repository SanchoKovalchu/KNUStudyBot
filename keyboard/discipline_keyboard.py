from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from bot_create import cursor

sql = 'SELECT sb_full_name FROM disciplines'
cursor.execute(sql)
list = []
for item in cursor.fetchall():
    list.append(item["sb_full_name"])

dsp_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True, one_time_keyboard=True)
dsp_keyboard.add(*list)