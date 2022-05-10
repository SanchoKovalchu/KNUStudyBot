from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from keyboard.material_keyboard import mtrl_keyboard
from handlers.login import UserRoles

async def material_command(message: types.Message, state: FSMContext):
    # Set state
    await message.reply("Що зробити?", reply_markup=mtrl_keyboard)


def register_handlers_teacher(dp: Dispatcher):
    dp.register_message_handler(material_command, lambda message: message.text == "Матеріал", state=UserRoles.teacher)
