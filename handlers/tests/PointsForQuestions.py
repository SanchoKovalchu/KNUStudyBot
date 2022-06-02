from aiogram import types, Dispatcher
from handlers.tests import AddTest
from handlers.login import UserRoles
from aiogram.dispatcher.filters.state import State, StatesGroup

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

class InputCost(StatesGroup):
    input_cost = State()
    agree_cost = State()
    final = State()

key = {}

async def final_keyboard():
    buttons = [types.InlineKeyboardButton(text="Не зберігати", callback_data="m_A1"),
               types.InlineKeyboardButton(text="Зберегти", callback_data="m_A2")]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard

async def get_keyboard_value():
    buttons = [types.InlineKeyboardButton(text="Змінити", callback_data="e_A1"),
               types.InlineKeyboardButton(text="Підтвердити", callback_data="e_A2")]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard

async def update_num_value2(num: int, numofquestions: int, answervars, question_value, question, message: types.Message, keyb):
    key[message.from_user.id] = keyb
    if num == numofquestions:
        await InputCost.final.set()
        await message.edit_text("Зберегти тест?\n", reply_markup=await final_keyboard())
    else:
        await InputCost.input_cost.set()
        stringofans = ""
        for i in range(0, len(answervars[num])):
            stringofans = stringofans + answervars[num][i] + "\n"
        if question_value[num] == -1:
            await message.edit_text("Введіть кількість балів за це питання\n\n" + "Питання " + str(num + 1) + "\n" + question[num] + "\nВаріанти відповідей: \n" + stringofans)
        else:
            await message.edit_text("Введіть кількість балів за це питання\n\n" + "Питання " + str(num + 1) + "\n" + question[num] + "\nВаріанти відповідей: \n" + stringofans + "Ваша відповідь: \n" + question_value[num])

async def update_num_value(num: int, numofquestions: int, answervars, question_value, question, message: types.Message):
    if num == numofquestions:
        await InputCost.final.set()
        await message.edit_text("Зберегти тест?\n", reply_markup=await final_keyboard())
    else:
        await InputCost.input_cost.set()
        stringofans = ""
        for i in range(0, len(answervars[num])):
            stringofans = stringofans + answervars[num][i] + "\n"
        if question_value[num] == -1:
            await message.edit_text("Введіть кількість балів за це питання\n\n" + "Питання " + str(num + 1) + "\n" + question[num] + "\nВаріанти відповідей: \n" + stringofans)
        else:
            await message.edit_text("Введіть кількість балів за це питання\n\n" + "Питання " + str(num + 1) + "\n" + question[num] + "\nВаріанти відповідей: \n" + stringofans + "Ваша відповідь: \n" + question_value[num])

async def input_question_value(message: types.Message):
    try:
        AddTest.user_question_value[message.from_user.id][AddTest.user_tasknumber.get(message.from_user.id, 0)] = float(message.text)
        if (float(message.text) <= 0):
            AddTest.user_question_value[message.from_user.id][AddTest.user_tasknumber.get(message.from_user.id, 0)] = float(-1)
            await message.answer("Введено некоректне значення. Введіть іншу кількість балів.")
        else:
            await InputCost.agree_cost.set()
            await message.answer("Ви підтверджуєте введені бали?\n" + message.text, reply_markup=await get_keyboard_value())
    except:
        AddTest.user_question_value[message.from_user.id][AddTest.user_tasknumber.get(message.from_user.id, 0)] = float(-1)
        await message.answer("Введено некоректне значення. Введіть іншу кількість балів.")

async def callbacks_agree_value(call: types.CallbackQuery):
    print(key)
    print(call.from_user.id)
    await InputCost.input_cost.set()
    action = call.data.split("_")[1]
    if action == "A1":
        AddTest.user_question_value[call.message.from_user.id][AddTest.user_tasknumber.get(call.message.from_user.id, 0)] = float(-1)
        await call.message.edit_text("Введіть іншу кількість балів")
    else:
        keyb = key.get(call.message.from_user.id, 0)
        AddTest.user_tasknumber[keyb] = AddTest.user_tasknumber.get(keyb, 0) + int(1)
        question = AddTest.user_question.get(keyb, 0)
        print(question)
        num = len(question)
        print(question)
        await update_num_value(num, len(AddTest.user_question.get(keyb)), AddTest.user_answervars.get(keyb), AddTest.user_question_value.get(keyb), AddTest.user_question.get(keyb), call.message)

async def callbacks_final(call: types.CallbackQuery):
    await InputCost.input_cost.set()
    action = call.data.split("_")[1]
    if action == "A1":
        await call.message.edit_text("Дії відхилено, тест не збережено!")
        await UserRoles.teacher.set()
    else:
        print()
        print()
        print()
        print()
        print()
        print(AddTest.user_subject.get(call.from_user.id))
        print(AddTest.user_numofquestions.get(call.from_user.id))
        print(AddTest.user_question.get(call.from_user.id))
        print(AddTest.user_numofvars.get(call.from_user.id))
        print(AddTest.user_answervars.get(call.from_user.id))
        print(AddTest.user_answerstring.get(call.from_user.id))
        await call.message.edit_text("Тест створено успішно!")
        await UserRoles.teacher.set()

def register_handlers_points(dp: Dispatcher):
    dp.register_callback_query_handler(callbacks_agree_value, state=InputCost.agree_cost)
    dp.register_message_handler(input_question_value, state=InputCost.input_cost)
    dp.register_callback_query_handler(callbacks_final, state=InputCost.final)