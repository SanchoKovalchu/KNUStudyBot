from aiogram.dispatcher.filters import Text
from aiogram import types, Dispatcher

user_data = {}
user_task = {}
user_answersave = {}

answerstring = "ABB"
question = ["Question1Text", "Question2Text", "Question3Text"]
numofquestions = [2, 4, 3]
answervarA = ["Answer 1A", "Answer2A", "Answer3A", "Answer4A"]
answervarB = ["Answer 1B", "Answer2B", "Answer3B", "Answer4B"]
answervarC = ["Answer 1C", "Answer2C", "Answer3C", "Answer4C"]
answervarD = ["Answer 1D", "Answer2D", "Answer3D", "Answer4D"]

def get_keyboard(num: int, line):
    if str(line)[num] == '_':
        if num == 0:
            if numofquestions[0] == 2:
                buttons = [types.InlineKeyboardButton(text="A", callback_data="ans_A"),
                           types.InlineKeyboardButton(text="B", callback_data="ans_B"),
                           types.InlineKeyboardButton(text="Next", callback_data="ans_Next")]
                keyboard = types.InlineKeyboardMarkup(row_width=2)
                keyboard.add(*buttons)
                return keyboard
            elif numofquestions[0] == 3:
                buttons = [types.InlineKeyboardButton(text="A", callback_data="ans_A"),
                           types.InlineKeyboardButton(text="B", callback_data="ans_B"),
                           types.InlineKeyboardButton(text="C", callback_data="ans_C"),
                           types.InlineKeyboardButton(text="Next", callback_data="ans_Next")]
                keyboard = types.InlineKeyboardMarkup(row_width=3)
                keyboard.add(*buttons)
                return keyboard
            else:
                buttons = [types.InlineKeyboardButton(text="A", callback_data="ans_A"),
                           types.InlineKeyboardButton(text="B", callback_data="ans_B"),
                           types.InlineKeyboardButton(text="C", callback_data="ans_C"),
                           types.InlineKeyboardButton(text="D", callback_data="ans_D"),
                           types.InlineKeyboardButton(text="Next", callback_data="ans_Next")]
                keyboard = types.InlineKeyboardMarkup(row_width=4)
                keyboard.add(*buttons)
                return keyboard
        elif num != len(answerstring) - 1:
            if numofquestions[num] == 2:
                buttons = [types.InlineKeyboardButton(text="A", callback_data="ans_A"),
                           types.InlineKeyboardButton(text="B", callback_data="ans_B"),
                           types.InlineKeyboardButton(text="Previous", callback_data="ans_Previous"),
                           types.InlineKeyboardButton(text="Next", callback_data="ans_Next")]
                keyboard = types.InlineKeyboardMarkup(row_width=2)
                keyboard.add(*buttons)
                return keyboard
            elif numofquestions[num] == 3:
                buttons = [types.InlineKeyboardButton(text="A", callback_data="ans_A"),
                           types.InlineKeyboardButton(text="B", callback_data="ans_B"),
                           types.InlineKeyboardButton(text="C", callback_data="ans_C"),
                           types.InlineKeyboardButton(text="Previous", callback_data="ans_Previous"),
                           types.InlineKeyboardButton(text="Next", callback_data="ans_Next")]
                keyboard = types.InlineKeyboardMarkup(row_width=3)
                keyboard.add(*buttons)
                return keyboard
            else:
                buttons = [types.InlineKeyboardButton(text="A", callback_data="ans_A"),
                           types.InlineKeyboardButton(text="B", callback_data="ans_B"),
                           types.InlineKeyboardButton(text="C", callback_data="ans_C"),
                           types.InlineKeyboardButton(text="D", callback_data="ans_D"),
                           types.InlineKeyboardButton(text="Previous", callback_data="ans_Previous"),
                           types.InlineKeyboardButton(text="Next", callback_data="ans_Next")]
                keyboard = types.InlineKeyboardMarkup(row_width=4)
                keyboard.add(*buttons)
                return keyboard
        else:
            if numofquestions[num] == 2:
                buttons = [types.InlineKeyboardButton(text="A", callback_data="ans_A"),
                           types.InlineKeyboardButton(text="B", callback_data="ans_B"),
                           types.InlineKeyboardButton(text="Previous", callback_data="ans_Previous"),
                           types.InlineKeyboardButton(text="End", callback_data="ans_End")]
                keyboard = types.InlineKeyboardMarkup(row_width=2)
                keyboard.add(*buttons)
                return keyboard
            elif numofquestions[num] == 3:
                buttons = [types.InlineKeyboardButton(text="A", callback_data="ans_A"),
                           types.InlineKeyboardButton(text="B", callback_data="ans_B"),
                           types.InlineKeyboardButton(text="C", callback_data="ans_C"),
                           types.InlineKeyboardButton(text="Previous", callback_data="ans_Previous"),
                           types.InlineKeyboardButton(text="End", callback_data="ans_End")]
                keyboard = types.InlineKeyboardMarkup(row_width=3)
                keyboard.add(*buttons)
                return keyboard
            else:
                buttons = [types.InlineKeyboardButton(text="A", callback_data="ans_A"),
                           types.InlineKeyboardButton(text="B", callback_data="ans_B"),
                           types.InlineKeyboardButton(text="C", callback_data="ans_C"),
                           types.InlineKeyboardButton(text="D", callback_data="ans_D"),
                           types.InlineKeyboardButton(text="Previous", callback_data="ans_Previous"),
                           types.InlineKeyboardButton(text="End", callback_data="ans_End")]
                keyboard = types.InlineKeyboardMarkup(row_width=4)
                keyboard.add(*buttons)
                return keyboard
    else:
        if num == 0:
            buttons = [types.InlineKeyboardButton(text="Change answer", callback_data="ans_Change"),
                       types.InlineKeyboardButton(text="Next", callback_data="ans_Next")]
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            keyboard.add(*buttons)
            return keyboard
        elif num != len(answerstring) - 1:
            buttons = [types.InlineKeyboardButton(text="Change answer", callback_data="ans_Change"),
                       types.InlineKeyboardButton(text="Previous", callback_data="ans_Previous"),
                       types.InlineKeyboardButton(text="Next", callback_data="ans_Next")]
            keyboard = types.InlineKeyboardMarkup(row_width=3)
            keyboard.add(*buttons)
            return keyboard
        else:
            buttons = [types.InlineKeyboardButton(text="Change answer", callback_data="ans_Change"),
                       types.InlineKeyboardButton(text="Previous", callback_data="ans_Previous"),
                       types.InlineKeyboardButton(text="End", callback_data="ans_End")]
            keyboard = types.InlineKeyboardMarkup(row_width=3)
            keyboard.add(*buttons)
            return keyboard

async def cmd_numbers(message: types.Message):
    user_data[message.from_user.id] = 0
    user_task[message.from_user.id] = 0
    stringstr = ""
    for i in range(0, len(answerstring)):
        stringstr = stringstr + "_"
    user_answersave[message.from_user.id] = stringstr
    if numofquestions[0] == 2:
        await message.answer("Питання 1\n" + question[0] + "\nОберіть відповідь: \n" + answervarA[0] + "\n" + answervarB[0], reply_markup=get_keyboard(0, stringstr))
    elif numofquestions[0] == 3:
        await message.answer("Питання 1\n" + question[0] + "\nОберіть відповідь: \n" + answervarA[0] + "\n" + answervarB[0] + "\n" + answervarC[0], reply_markup=get_keyboard(0, stringstr))
    else:
        await message.answer("Питання 1\n" + question[0] + "\nОберіть відповідь: \n" + answervarA[0] + "\n" + answervarB[0] + "\n" + answervarC[0] + "\n" + answervarD[0], reply_markup=get_keyboard(0, stringstr))

async def update_num_text(message: types.Message, task_number: int, user_savedans):
    #Оновлення тексту питань
    if numofquestions[task_number] == 2:
        await message.edit_text("Питання " + str(task_number + 1) + "\n" + question[task_number] + "\nОберіть відповідь: \n" + answervarA[task_number] + "\n" + answervarB[task_number], reply_markup=get_keyboard(task_number, user_savedans))
    elif numofquestions[task_number] == 3:
        await message.edit_text("Питання " + str(task_number + 1) + "\n" + question[task_number] + "\nОберіть відповідь: \n" + answervarA[task_number] + "\n" + answervarB[task_number] + "\n" + answervarC[task_number], reply_markup=get_keyboard(task_number, user_savedans))
    else:
        await message.edit_text("Питання " + str(task_number + 1) + "\n" + question[task_number] + "\nОберіть відповідь: \n" + answervarA[task_number] + "\n" + answervarB[task_number] + "\n" + answervarC[task_number] + "\n" + answervarD[task_number], reply_markup=get_keyboard(task_number, user_savedans))

async def callbacks_num(call: types.CallbackQuery):
    user_value = user_data.get(call.from_user.id, 0)
    user_tasknumber = user_task.get(call.from_user.id, 0)
    user_savedans = user_answersave.get(call.from_user.id, 0)
    action = call.data.split("_")[1]
    if action == "A" or action == "B" or action == "C" or action == "D":
        stringstr = user_savedans
        stringstr = stringstr[:user_tasknumber] + str(action) + stringstr[user_tasknumber + 1:]
        user_answersave[call.from_user.id] = stringstr
        await update_num_text(call.message, user_tasknumber, stringstr)
    elif action == "Next":
        user_task[call.from_user.id] = user_tasknumber + 1
        await update_num_text(call.message, user_tasknumber + 1, user_savedans)
    elif action == "Previous":
        user_task[call.from_user.id] = user_tasknumber - 1
        await update_num_text(call.message, user_tasknumber - 1, user_savedans)
    elif action == "Change":
        stringstr = user_savedans
        stringstr = stringstr[:user_tasknumber] + "_" + stringstr[user_tasknumber + 1:]
        user_answersave[call.from_user.id] = stringstr
        await update_num_text(call.message, user_tasknumber, stringstr)
    else:
        for i in range(0, len(answerstring)):
            if user_savedans[i] == answerstring[i]:
                user_value = user_value + 1
        await call.message.edit_text(f"Сума балів: {user_value}")
    await call.answer()

def register_handlers_tests(dp: Dispatcher):
    dp.register_message_handler(cmd_numbers, commands="choose")
    dp.register_callback_query_handler(callbacks_num, Text(startswith="ans_"))