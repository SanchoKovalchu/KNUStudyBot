from aiogram import types, Dispatcher
from handlers.tests import AddTest, PointsForQuestions
from aiogram.dispatcher.filters.state import State, StatesGroup

alphabet = "ABCDEFGHIJ"

class InputCorrect(StatesGroup):
    input_correct = State()

async def get_keyboard(num: int, line, numofvars):
    buttons = []
    if str(line)[num] == '_':
        if num != 0:
            buttons.append(types.InlineKeyboardButton(text="Previous", callback_data="ans_Previous"))
        for i in range(0, numofvars[num]):
            buttons.append(types.InlineKeyboardButton(text=alphabet[i], callback_data="ans_" + alphabet[i]))
        if num != len(line) - 1:
            buttons.append(types.InlineKeyboardButton(text="Next", callback_data="ans_Next"))
        else:
            buttons.append(types.InlineKeyboardButton(text="End", callback_data="ans_End"))
        keyboard = types.InlineKeyboardMarkup(row_width=4)
        keyboard.add(*buttons)
        return keyboard
    else:
        l = int(1)
        if num != 0:
            l = l + 1
            buttons.append(types.InlineKeyboardButton(text="Previous", callback_data="ans_Previous"))
        buttons.append(types.InlineKeyboardButton(text="Change answer", callback_data="ans_Change"))
        if num != len(line) - 1:
            l = l + 1
            buttons.append(types.InlineKeyboardButton(text="Next", callback_data="ans_Next"))
        else:
            l = l + 1
            buttons.append(types.InlineKeyboardButton(text="End", callback_data="ans_End"))
        keyboard = types.InlineKeyboardMarkup(row_width=l)
        keyboard.add(*buttons)
        return keyboard

async def update_num_text(line, num: int, answervars, question, numofvars, message: types.Message):
    stringofans = ""
    for i in range(0, len(answervars[num])):
        stringofans = stringofans + answervars[num][i] + "\n"
    if line[num] == '_':
        await message.edit_text("Питання " + str(num + 1) + "\n" + question[num] + "\nОберіть правильну відповідь: \n" + stringofans, reply_markup=await get_keyboard(num, line, numofvars))
    else:
        await message.edit_text("Питання " + str(num + 1) + "\n" + question[num] + "\nВаріанти відповіді: \n" + stringofans + "Ви позначили як правильну: " + line[num], reply_markup=await get_keyboard(num, line, numofvars))

async def callbacks_num(call: types.CallbackQuery):
    user_savedans = AddTest.user_answerstring.get(call.from_user.id, 0)
    action = call.data.split("_")[1]
    if action == "Next":
        AddTest.user_tasknumber[call.from_user.id] = AddTest.user_tasknumber.get(call.from_user.id, 0) + 1
        answervars = AddTest.user_answervars.get(call.from_user.id, 0)
        question = AddTest.user_question.get(call.from_user.id, 0)
        numofvars = AddTest.user_numofvars.get(call.from_user.id, 0)
        await update_num_text(user_savedans, AddTest.user_tasknumber.get(call.from_user.id, 0), answervars, question, numofvars, call.message)
    elif action == "Previous":
        AddTest.user_tasknumber[call.from_user.id] = AddTest.user_tasknumber.get(call.from_user.id, 0) - 1
        answervars = AddTest.user_answervars.get(call.from_user.id, 0)
        question = AddTest.user_question.get(call.from_user.id, 0)
        numofvars = AddTest.user_numofvars.get(call.from_user.id, 0)
        await update_num_text(user_savedans, AddTest.user_tasknumber.get(call.from_user.id, 0), answervars, question, numofvars, call.message)
    elif action == "Change":
        stringstr = user_savedans
        stringstr = stringstr[:AddTest.user_tasknumber.get(call.from_user.id, 0)] + "_" + stringstr[AddTest.user_tasknumber.get(call.from_user.id, 0) + 1:]
        AddTest.user_answerstring[call.from_user.id] = stringstr
        answervars = AddTest.user_answervars.get(call.from_user.id, 0)
        question = AddTest.user_question.get(call.from_user.id, 0)
        numofvars = AddTest.user_numofvars.get(call.from_user.id, 0)
        await update_num_text(stringstr, AddTest.user_tasknumber.get(call.from_user.id, 0), answervars, question, numofvars, call.message)
    elif action == "End":
        await PointsForQuestions.InputCost.input_cost.set()
        #print(AddTest.user_subject.get(call.from_user.id))
        #numofquestions = AddTest.user_numofquestions.get(call.from_user.id, 0)
        question = AddTest.user_question.get(call.from_user.id, 0)
        question_value = AddTest.user_question_value.get(call.from_user.id, 0)
        #numofvars = AddTest.user_numofvars.get(call.from_user.id, 0)
        answervars = AddTest.user_answervars.get(call.from_user.id, 0)
        keyb = call.from_user.id
        print(keyb)
        await PointsForQuestions.update_num_value2(0, len(question), answervars, question_value, question, call.message, keyb)
    else:
        stringstr = user_savedans
        stringstr = stringstr[:AddTest.user_tasknumber.get(call.from_user.id, 0)] + str(action) + stringstr[AddTest.user_tasknumber.get(call.from_user.id, 0) + 1:]
        AddTest.user_answerstring[call.from_user.id] = stringstr
        answervars = AddTest.user_answervars.get(call.from_user.id, 0)
        question = AddTest.user_question.get(call.from_user.id, 0)
        numofvars = AddTest.user_numofvars.get(call.from_user.id, 0)
        await update_num_text(stringstr, AddTest.user_tasknumber.get(call.from_user.id, 0), answervars, question, numofvars, call.message)
    await call.answer()

def register_handlers_correctanswer(dp: Dispatcher):
    dp.register_callback_query_handler(callbacks_num, state=InputCorrect.input_correct)