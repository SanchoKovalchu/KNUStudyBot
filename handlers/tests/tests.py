from aiogram import types, Dispatcher
from handlers.tests import test_json_decoder
from handlers.login import UserRoles
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboard.discipline_keyboard import dsp_keyboard, disciplines
from keyboard.student_keyboard import st_keyboard
from bot_create import cursor, bot, connection

alphabet = "ABCDEFGHIJ"

user_subject = {}
user_data = {}
user_answersave = {}
user_userans = {}
user_tasknumber = {}
user_answerstring = {}
user_question = {}
user_question_value = {}
user_answervars = {}
user_numofvars = {}

class TestingInp(StatesGroup):
    testing = State()
    choosing_subject = State()

async def get_keyboard(num: int, num2: int, numoftests: int, line, numofvars, message: types.Message):
    buttons = []
    if num2 == 1:
        l = int(1)
        if numoftests == 1:
            buttons.append(types.InlineKeyboardButton(text="Choose", callback_data="ans_Ch2"))
        else:
            if num != 0:
                l = l + 1
                buttons.append(types.InlineKeyboardButton(text="<-", callback_data="ans_Previous"))
            buttons.append(types.InlineKeyboardButton(text="Choose", callback_data="ans_Ch2"))
            if num != numoftests - 1:
                l = l + 1
                buttons.append(types.InlineKeyboardButton(text="->", callback_data="ans_Next"))
        keyboard = types.InlineKeyboardMarkup(row_width=l)
        keyboard.add(*buttons)
        return keyboard
    else:
        if str(line)[num] == '_':
            if num != 0:
                buttons.append(types.InlineKeyboardButton(text="Previous", callback_data="ans_Previous"))
            for i in range(0, numofvars[num]):
                buttons.append(types.InlineKeyboardButton(text=alphabet[i], callback_data="ans_"+alphabet[i]))
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

async def choose_subject(message: types.Message):
    await TestingInp.choosing_subject.set()
    await bot.send_message(message.chat.id, "Оберіть назву предмета", reply_markup=dsp_keyboard)

async def choosed_subject(message : types.Message):
    user_subject[message.from_user.id] = message.text
    await test_json_decoder.count_tests(message.text, message)
    if (test_json_decoder.numoftests.get(message.from_user.id, 0) == 0):
        await message.answer("Немає тестів з цього предмета")
        await UserRoles.student.set()
    elif (test_json_decoder.numoftests.get(message.from_user.id, 0) == 1):
        await TestingInp.testing.set()
        test_json_decoder.num2[message.from_user.id] = int(1)
        test_json_decoder.num3[message.from_user.id] = int(test_json_decoder.numoftests[message.from_user.id]) - 1
        user_tasknumber[message.from_user.id] = int(0)
        user_userans[message.from_user.id] = ""
        await message.answer("Оберіть номер тесту\n" + "\nПоточний тест: " + str(1), reply_markup=await get_keyboard(0, 1, test_json_decoder.numoftests.get(message.from_user.id, 0), "", [], message))
    else:
        await TestingInp.testing.set()
        test_json_decoder.num2[message.from_user.id] = int(1)
        test_json_decoder.num3[message.from_user.id] = int(test_json_decoder.numoftests[message.from_user.id]) - 1
        user_tasknumber[message.from_user.id] = int(0)
        user_userans[message.from_user.id] = ""
        await message.answer("Оберіть номер тесту\n" + "\nПоточний тест: " + str(1), reply_markup=await get_keyboard(0, 1, test_json_decoder.numoftests.get(message.from_user.id, 0), "", [], message))

async def update_num_text(line, num: int, num2: int, numoftests: int, answervars, question, numofvars, message: types.Message):
    if num2 == 1:
        await message.edit_text("Оберіть номер тесту\n" + "\nПоточний тест: " + str(num + 1), reply_markup=await get_keyboard(num, num2, numoftests, line, 0, message))
    else:
        stringofans = ""
        for i in range(0, len(answervars[num])):
            stringofans = stringofans + answervars[num][i] + "\n"
        if line[num] == '_':
            await message.edit_text("Питання " + str(num + 1) + "\n" + question[num] + "\nОберіть відповідь: \n" + stringofans, reply_markup=await get_keyboard(num, num2, 0, line, numofvars, message))
        else:
            await message.edit_text("Питання " + str(num + 1) + "\n" + question[num] + "\nВаріанти відповіді: \n" + stringofans + "Ваша відповідь: \n" + line[num], reply_markup=await get_keyboard(num, num2, 0, line, numofvars, message))

async def callbacks_num(call: types.CallbackQuery):
    user_value = user_data.get(call.from_user.id, 0)
    user_savedans = user_userans.get(call.from_user.id, 0)
    num2 = test_json_decoder.num2.get(call.from_user.id, 0)
    numoftests = test_json_decoder.numoftests.get(call.from_user.id, 0)
    action = call.data.split("_")[1]
    if action == "Ch2":
        test_json_decoder.num2[call.from_user.id] = int(2)
        test_json_decoder.numoftest[call.from_user.id] = user_tasknumber.get(call.from_user.id, 0)
        user_tasknumber[call.from_user.id] = 0
        await test_json_decoder.get_info(call)
        stringstr = ""
        answerstring = user_answerstring.get(call.from_user.id, 0)
        for i in range(0, len(answerstring)):
            stringstr = stringstr + "_"
        user_userans[call.from_user.id] = stringstr
        answervars = user_answervars.get(call.from_user.id, 0)
        question = user_question.get(call.from_user.id, 0)
        numofvars = user_numofvars.get(call.from_user.id, 0)
        await update_num_text(stringstr, 0, 2, numoftests, answervars, question, numofvars, call.message)
    elif action == "Next":
        user_tasknumber[call.from_user.id] = user_tasknumber.get(call.from_user.id, 0) + 1
        answervars = []
        question = []
        numofvars = []
        if test_json_decoder.num2.get(call.from_user.id, 0) == 2:
            answervars = user_answervars.get(call.from_user.id, 0)
            question = user_question.get(call.from_user.id, 0)
            numofvars = user_numofvars.get(call.from_user.id, 0)
        await update_num_text(user_savedans, user_tasknumber.get(call.from_user.id, 0), num2, numoftests, answervars, question, numofvars, call.message)
    elif action == "Previous":
        user_tasknumber[call.from_user.id] = user_tasknumber.get(call.from_user.id, 0) - 1
        answervars = []
        question = []
        numofvars = []
        if test_json_decoder.num2.get(call.from_user.id, 0) == 2:
            answervars = user_answervars.get(call.from_user.id, 0)
            question = user_question.get(call.from_user.id, 0)
            numofvars = user_numofvars.get(call.from_user.id, 0)
        await update_num_text(user_savedans, user_tasknumber.get(call.from_user.id, 0), num2, numoftests, answervars, question, numofvars, call.message)
    elif action == "Change":
        stringstr = user_savedans
        stringstr = stringstr[:user_tasknumber.get(call.from_user.id, 0)] + "_" + stringstr[user_tasknumber.get(call.from_user.id, 0) + 1:]
        user_userans[call.from_user.id] = stringstr
        answervars = user_answervars.get(call.from_user.id, 0)
        question = user_question.get(call.from_user.id, 0)
        numofvars = user_numofvars.get(call.from_user.id, 0)
        await update_num_text(stringstr, user_tasknumber.get(call.from_user.id, 0), num2, numoftests, answervars, question, numofvars, call.message)
    elif action == "End":
        answerstring = user_answerstring.get(call.from_user.id, 0)
        for i in range(0, len(answerstring)):
            if user_savedans[i] == answerstring[i]:
                user_value = user_value + user_question_value.get(call.from_user.id, 0)[i]
        await UserRoles.student.set()
        await call.message.edit_text(f"Тест пройдено! Ваша оцінка: {user_value}")
        await bot.send_message(call.from_user.id, "Оберіть подальші дії", reply_markup=st_keyboard)
    else:
        stringstr = user_savedans
        stringstr = stringstr[:user_tasknumber.get(call.from_user.id, 0)] + str(action) + stringstr[user_tasknumber.get(call.from_user.id, 0) + 1:]
        user_userans[call.from_user.id] = stringstr
        answervars = user_answervars.get(call.from_user.id, 0)
        question = user_question.get(call.from_user.id, 0)
        numofvars = user_numofvars.get(call.from_user.id, 0)
        await update_num_text(stringstr, user_tasknumber.get(call.from_user.id, 0), num2, numoftests, answervars, question, numofvars, call.message)
    await call.answer()

def register_handlers_tests(dp: Dispatcher):
    dp.register_message_handler(choose_subject, lambda message: message.text == "Тестування", state=UserRoles.student)
    dp.register_message_handler(choosed_subject, state=TestingInp.choosing_subject)
    dp.register_callback_query_handler(callbacks_num, state=TestingInp.testing)