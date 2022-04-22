import logging
  
import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor
 
logging.basicConfig(level=logging.INFO)
 
API_TOKEN = '5302840148:AAGtGfjfQZWbwRn0mqPrv_rEqRhK9XEiarg'
 
 
bot = Bot(token=API_TOKEN)
 
# For example use simple MemoryStorage for Dispatcher.
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
 
# States
class Form(StatesGroup):
    login = State()  # Will be represented in storage as 'Form:login'
    password = State()  # Will be represented in storage as 'Form:password'
    course = State()  # Will be represented in storage as 'Form:course'
    group = State()  # Will be represented in storage as 'Form:course'

@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):

     # Set state
     await Form.login.set()
 
     await message.reply("Твій логін")
 
 
 # You can use state '*' if you need to handle all states
@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):

    current_state = await state.get_state()
    if current_state is None:
        return
 
    logging.info('Cancelling state %r', current_state)
    # Cancel state and inform user about it
    await state.finish()
    # And remove keyboard (just in case)
    await message.reply('Cancelled.', reply_markup=types.ReplyKeyboardRemove())
 
 
@dp.message_handler(state=Form.login)
async def process_name(message: types.Message, state: FSMContext):

    async with state.proxy() as data:
        data['login'] = message.text
 
    await Form.next()
    await message.reply("Твій пароль")
 
 
# # Check age. Age gotta be digit
# @dp.message_handler(lambda message: not message.text.isdigit(), state=Form.password)
# async def process_age_invalid(message: types.Message):
#
#     return await message.reply("Age gotta be a number.\nHow old are you? (digits only)")
 
 
@dp.message_handler(state=Form.password)
async def process_age(message: types.Message, state: FSMContext):
    # Update state and data
    async with state.proxy() as data:
        data['password'] = message.text
    await Form.next()

    # Configure ReplyKeyboardMarkup
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("1", "2", "3", "4")
 
    await message.answer("Твій курс?", reply_markup=markup)


@dp.message_handler(lambda message: message.text not in ["1", "2", "3", "4"], state=Form.course)
async def process_gender_invalid(message: types.Message):

   return await message.reply("Bad option. Choose your course from the keyboard.")


@dp.message_handler(state=Form.course)
async def process_gender(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['course'] = message.text
        await Form.next()

        # Configure ReplyKeyboardMarkup
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        markup.add("IPZ-#1", "IPZ-#2", "IPZ-#3", "IPZ-#4")

        await message.answer("Твоя групу?", reply_markup=markup)


@dp.message_handler(lambda message: message.text not in ["IPZ-#1", "IPZ-#2", "IPZ-#3", "IPZ-#4"], state=Form.group)
async def process_gender_invalid(message: types.Message):

   return await message.reply("Bad option. Choose your group from the keyboard.")


@dp.message_handler(state=Form.group)
async def process_age(message: types.Message, state: FSMContext):
    # Update state and data
    async with state.proxy() as data:
        data['group'] = message.text
        markup = types.ReplyKeyboardRemove()
        await bot.send_message(
            message.chat.id,
            md.text(
                md.text('Логін', md.bold(data['login'])),
                md.text('Пароль:', md.code(data['password'])),
                md.text('Курс:', data['course']),
                md.text('Група:', data['group']),
                sep='\n',
            ),
            reply_markup=markup,
            parse_mode=ParseMode.MARKDOWN,
        )
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)