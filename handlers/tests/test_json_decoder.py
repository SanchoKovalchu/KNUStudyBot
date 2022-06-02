import json
from bot_create import cursor
from handlers.tests import tests
from aiogram import types

num2 = {}
num3 = {}
numoftest = {}
numoftests = {}
subject = {}

async def count_tests(line, message: types.Message):
    sql = "SELECT * FROM teachers_tests WHERE test_subject = %s"
    numoftests[message.from_user.id] = cursor.execute(sql, line)

async def get_info(call: types.CallbackQuery):
    sql = "SELECT * FROM teachers_tests WHERE test_owner = %s AND test_subject = %s AND test_name = %s"
    cursor.execute(sql, (0, subject.get(call.from_user.id, 0), "Тест " + str(numoftest.get(call.from_user.id, 0) + 1)))
    for row in cursor:
        json_string = row["test_info"]
    json_string_decoded = json.loads(json_string)
    tests.user_answerstring[call.from_user.id] = json_string_decoded["answerstring"]
    tests.user_numofvars[call.from_user.id] = json_string_decoded["numofvars"]
    tests.user_question[call.from_user.id] = json_string_decoded["question"]
    tests.user_answervars[call.from_user.id] = json_string_decoded["answervars"]
    tests.user_question_value[call.from_user.id] = json_string_decoded["question_value"]