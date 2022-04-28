from aiogram import types, Dispatcher
from keyboard.material_keyboard import mtrl_keyboard


async def material_command(message: types.Message):
    # Set state
    await message.reply("Що зробити?", reply_markup=mtrl_keyboard)


def register_handlers_teacher(dp: Dispatcher):
    dp.register_message_handler(material_command, lambda message: message.text == "Матеріал")
