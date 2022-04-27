from aiogram import types, Dispatcher
from bot_create import bot


async def cm_start(message : types.Message):
    await bot.send_message(message.chat.id,"Видалити матеріал")


def register_handlers_add_material(dp : Dispatcher):
    dp.register_message_handler(cm_start, lambda message: message.text == "Видалити матеріал", state=None)
