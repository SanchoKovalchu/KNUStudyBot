import logging
from aiogram import executor, types
from handlers import login
from handlers import register
from handlers import photo_loader
from handlers.teacher_material_dir import add_material
from handlers.teacher_material_dir import edit_material
from handlers.teacher_material_dir import delete_material
from bot_create import dp
from keyboard import first_keyboard
from user_role_files import teacher

photo_loader.register_handlers_files(dp)
login.register_handlers_login(dp)
register.register_handlers_register(dp)
teacher.register_handlers_teacher(dp)
add_material.register_handlers_add_material(dp)
edit_material.register_handlers_add_material(dp)
delete_material.register_handlers_add_material(dp)
logging.basicConfig(level=logging.INFO)


@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    await message.answer("Ласкаво прошу до StudyBot!", reply_markup=first_keyboard)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

