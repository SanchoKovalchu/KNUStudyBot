from aiogram import types, Dispatcher
from handlers.tests import CorrectAnswer, AddTest
from aiogram.dispatcher.filters.state import State, StatesGroup

class InputTexts(StatesGroup):
    input_choose = State()
    input_question_text = State()
    agree_question_text = State()
    input_ans = State()
    agree_ans = State()

async def get_create_keyboard():
    await InputTexts.input_choose.set()
    buttons = [types.InlineKeyboardButton(text="Додати варіант відповіді", callback_data="t_A1"),
               types.InlineKeyboardButton(text="Додати питання", callback_data="t_A2"),
               types.InlineKeyboardButton(text="Завершити заповнення питання", callback_data="t_A3")]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard

async def get_keyboard_agree():
    buttons = [types.InlineKeyboardButton(text="Змінити", callback_data="q_A1"),
               types.InlineKeyboardButton(text="Підтвердити", callback_data="q_A2")]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard

async def input_question_text(message: types.Message):
    num = AddTest.user_tasknumber.get(message.from_user.id, 0)
    AddTest.user_question[message.from_user.id][num] = message.text
    await InputTexts.agree_question_text.set()
    await message.answer("Ви підтверджуєте введені дані?\n" + message.text, reply_markup=await get_keyboard_agree())

async def input_ans_text(message: types.Message):
    AddTest.user_tempvars[message.from_user.id].append(message.text)
    await InputTexts.agree_ans.set()
    await message.answer("Ви підтверджуєте введені дані?\n" + message.text, reply_markup=await get_keyboard_agree())

async def callbacks_create(call: types.CallbackQuery):
    action = call.data.split("_")[1]
    if action == "A1":
        print(AddTest.user_numofvars.get(call.from_user.id)[AddTest.user_tasknumber.get(call.from_user.id)])
        if AddTest.user_numofvars.get(call.from_user.id)[AddTest.user_tasknumber.get(call.from_user.id)] < 10:
            await InputTexts.input_ans.set()
            await call.message.edit_text("Введіть варіант відповіді")
        else:
            await call.message.edit_text("Неможна створити більше 10 варіантів відповіді на одне питання")
            await call.message.answer("Оберіть дію\n", reply_markup=await get_create_keyboard())
    elif action == "A2":
        AddTest.user_answervars[call.from_user.id].append(AddTest.user_tempvars.get(call.from_user.id))
        AddTest.user_tempvars[call.from_user.id] = []
        AddTest.user_question[call.from_user.id].append("")
        AddTest.user_tasknumber[call.from_user.id] = AddTest.user_tasknumber.get(call.from_user.id) + 1
        AddTest.user_numofvars[call.from_user.id].append(0)
        await InputTexts.input_question_text.set()
        await call.message.edit_text("Введіть текст питання")
    else:
        AddTest.user_answervars[call.from_user.id].append(AddTest.user_tempvars.get(call.from_user.id))
        stringstr = ""
        for i in range(0, len(AddTest.user_question.get(call.from_user.id))):
            stringstr = stringstr + "_"
            AddTest.user_question_value[call.from_user.id].append(float(-1))
        AddTest.user_answerstring[call.from_user.id] = stringstr
        AddTest.user_tasknumber[call.from_user.id] = 0
        await CorrectAnswer.InputCorrect.input_correct.set()
        stringofans = ""
        for i in range(0, len(AddTest.user_answervars.get(call.from_user.id)[0])):
            stringofans = stringofans + AddTest.user_answervars.get(call.from_user.id)[0][i] + "\n"
        await call.message.edit_text("Питання " + str(1) + "\n" + AddTest.user_question.get(call.from_user.id)[0] + "\nОберіть правильну відповідь: \n" + stringofans, reply_markup=await CorrectAnswer.get_keyboard(0, stringstr, AddTest.user_numofvars.get(call.from_user.id)))

async def callbacks_agree_question(call: types.CallbackQuery):
    action = call.data.split("_")[1]
    if action == "A1":
        await InputTexts.input_question_text.set()
        await call.message.edit_text("Введіть виправлені дані")
    else:
        AddTest.user_numofquestions[call.from_user.id] = AddTest.user_numofquestions.get(call.from_user.id, 0) + 1
        await InputTexts.input_ans.set()
        await call.message.edit_text("Введіть варіант відповіді")

async def callbacks_agree_ans(call: types.CallbackQuery):
    action = call.data.split("_")[1]
    if action == "A1":
        AddTest.user_tempvars[call.from_user.id] = AddTest.user_tempvars.get(call.from_user.id, 0)[:-1]
        await InputTexts.input_ans.set()
        await call.message.edit_text("Введіть виправлені дані")
    else:
        num = AddTest.user_tasknumber.get(call.from_user.id, 0)
        AddTest.user_numofvars[call.from_user.id][num] = AddTest.user_numofvars.get(call.from_user.id, 0)[num] + 1
        if AddTest.user_numofvars.get(call.from_user.id, 0)[num] < 2:
            await InputTexts.input_ans.set()
            await call.message.edit_text("Введіть варіант відповіді")
        else:
            await call.message.edit_text("Оберіть дію\n", reply_markup=await get_create_keyboard())

def register_handlers_correct(dp: Dispatcher):
    dp.register_callback_query_handler(callbacks_create, state=InputTexts.input_choose)
    dp.register_callback_query_handler(callbacks_agree_question, state=InputTexts.agree_question_text)
    dp.register_callback_query_handler(callbacks_agree_ans, state=InputTexts.agree_ans)
    dp.register_message_handler(input_question_text, state=InputTexts.input_question_text)
    dp.register_message_handler(input_ans_text, state=InputTexts.input_ans)
