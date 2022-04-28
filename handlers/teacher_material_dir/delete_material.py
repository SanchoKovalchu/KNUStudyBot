from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import  State, StatesGroup
from aiogram import types, Dispatcher
from bot_create import bot

# class FSMFiles():


async def cm_start(message : types.Message):
    await bot.send_message(message.chat.id,"Видалити матеріал")


def register_handlers_files(dp : Dispatcher):
    dp.register_message_handler(cm_start, lambda message: message.text == "Видалити матеріал", state=None)
