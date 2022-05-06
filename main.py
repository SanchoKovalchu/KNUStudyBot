import logging
from aiogram import executor, types
from handlers import login
from handlers import announcement
from handlers import disciplines
from handlers import tests
from handlers import marks
from handlers.register_dir import admin_register
from handlers.register_dir import teacher_register
from handlers.register_dir import student_register
from handlers.teacher_material_dir import add_material
from handlers.teacher_material_dir import add_additional_material
from handlers.teacher_material_dir import edit_material
from handlers.teacher_material_dir import delete_material
from handlers.teacher_material_dir import view_material
from bot_create import dp, connection, cursor, bot
from keyboard import first_keyboard
from user_role_files import teacher
###
from threading import Thread
import aioschedule
import time
from datetime import datetime
import pymysql.cursors
import asyncio
###
add_material.register_handlers_files(dp)
add_additional_material.register_handlers_files(dp)
edit_material.register_handlers_files(dp)
delete_material.register_handlers_files(dp)
view_material.register_handlers_files(dp)
login.register_handlers_login(dp)
student_register.register_handlers_student_register(dp)
teacher_register.register_handlers_teacher_register(dp)
admin_register.register_handlers_admin_register(dp)
teacher.register_handlers_teacher(dp)
announcement.register_handlers_announcement(dp)
disciplines.register_handlers_disciplines(dp)
tests.register_handlers_tests(dp)
marks.register_handlers_marks(dp)
logging.basicConfig(level=logging.INFO)




@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    await message.answer("Ласкаво прошу до StudyBot!", reply_markup=first_keyboard)

async def send_message():
    sql = "SELECT * FROM add_file_storage"
    cursor.execute(sql)
    raw_dates_string = []
    file_id_array = []
    dates_array_for_comparing = []
    i = -1
    for row in cursor:
        i += 1
        print(i)
        raw_dates_string.append(row["date_time"])
        file_id_array.append(row["file_id"])
    print(raw_dates_string)
    print(file_id_array)

    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y %H:%M:%S")
    unixtime = datetime.strptime(str(dt_string), '%d-%m-%Y %H:%M:%S')
    unixtime_now = time.mktime(unixtime.timetuple())
    print(unixtime_now)
    for k in range(len(raw_dates_string)):
        date_string = raw_dates_string[k].split(', ')
        dates_array_for_comparing.append(date_string[0])
        if unixtime_now > float(dates_array_for_comparing[k]):
            print("YES")
    await bot.send_message(509032071, "Hello")


async def scheduler():
    aioschedule.every(300).seconds.do(send_message)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)

async def on_startup(_):
    asyncio.create_task(scheduler())

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False, on_startup=on_startup)



