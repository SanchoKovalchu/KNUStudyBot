from aiogram.dispatcher.filters import Text
from aiogram import types, Dispatcher
from handlers.tests import AddQuestions, PointsForQuestions, CorrectAnswer
from handlers.login import UserRoles
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboard.discipline_keyboard import dsp_keyboard, disciplines
from keyboard.teacher_keyboard import tch_keyboard
from bot_create import cursor, bot, connection

user_subject = {}

user_question = {}
user_numofvars = {}
user_answervars = {}
user_tasknumber = {}
user_Condition = {}
user_numofquestions = {}
user_tempvars = {}
user_toappend = {}
user_answerstring = {}
user_numofquestions = {}
user_question_value = {}

class CreatingTest(StatesGroup):
    creating = State()

async def add_test(message: types.Message):
    await CreatingTest.creating.set()
    await bot.send_message(message.chat.id, "Оберіть назву предмета", reply_markup=dsp_keyboard)

async def callbacks_subject(message: types.Message):
    user_subject[message.from_user.id] = message.text
    user_question[message.from_user.id] = []
    user_question[message.from_user.id].append("")
    user_numofvars[message.from_user.id] = []
    user_numofvars[message.from_user.id].append(0)
    user_answervars[message.from_user.id] = []
    user_tasknumber[message.from_user.id] = 0
    user_numofquestions[message.from_user.id] = 0
    user_tempvars[message.from_user.id] = []
    user_toappend[message.from_user.id] = ""
    user_answerstring[message.from_user.id] = ""
    user_numofquestions[message.from_user.id] = 0
    user_question_value[message.from_user.id] = []
    await AddQuestions.InputTexts.input_question_text.set()
    await message.answer("Введіть текст питання")

def register_handlers_addtest(dp: Dispatcher):
    dp.register_message_handler(add_test, lambda message: message.text == "Створити тест", state=UserRoles.teacher)
    dp.register_message_handler(callbacks_subject, state=CreatingTest.creating)