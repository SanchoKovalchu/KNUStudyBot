import logging
from aiogram import executor, types
from handlers import login
from handlers import register
from handlers import photo_loader
from bot_create import dp
from keyboard import st_keyboard
from keyboard import student_keyboard

photo_loader.register_handlers_files(dp)
login.register_handlers_login(dp)
register.register_handlers_register(dp)
student_keyboard.register_handlers_keyboard(dp)
logging.basicConfig(level=logging.INFO)


@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    await message.answer("Ласкаво прошу до StudyBot!", reply_markup=st_keyboard)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

