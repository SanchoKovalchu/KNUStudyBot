from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from bot_create import cursor, bot
from aiogram import types, Dispatcher

class Form(StatesGroup):
    subject = State()
    age = State()

async def announcement_command(message: types.Message):
    # Set state
    await Form.subject.set()
    # Connect to database
    sql = "SELECT sb_full_name AS subject FROM disciplines"
    cursor.execute(sql)
    # Creating markup
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    for row in cursor.fetchall():
        markup.add(row["subject"])
    markup.add("Продемонструвати всі одразу предмети")
    await bot.send_message(message.chat.id, text="Оберіть предмет, ща яким ви бажаєте отримати оцінки", reply_markup=markup)

async def view_marks(message : types.Message, state: FSMContext):
    # Local Variables
    subject_names = []
    the_message = ""
    summary_mark = 0

    # Getting the list of all the subjects in the bd
    async with state.proxy() as data:
        data['subject'] = message.text
        subject = data['subject']
    if subject != "Продемонструвати всі одразу предмети":
        sql = ("""SELECT 
        marks.Comment AS comment,
        marks.mark AS mark, 
        disciplines.sb_full_name AS subject 
        FROM marks INNER JOIN disciplines ON marks.id_subject = disciplines.id 
        WHERE marks.id_student  = '%s' AND 
        disciplines.sb_full_name = '%s'""") % (message.chat.id, subject)
    else:
        sql = ("""SELECT 
           marks.Comment AS comment,
           marks.mark AS mark, 
           disciplines.sb_full_name AS subject 
           FROM marks INNER JOIN disciplines ON marks.id_subject = disciplines.id 
           WHERE marks.id_student  = '%s' 
           ORDER BY subject""") % (message.chat.id)
    cursor.execute(sql)
    # Outputting results of elements
    for row in cursor.fetchall():
        if row["subject"] in subject_names:
            the_message += f'  {row["comment"]} :  {row["mark"]}\n'
            summary_mark += row["mark"]
        else:
            if len(subject_names) != 0:
                the_message += f'Оцінка в сумі: <b>{summary_mark}</b>\n'
            summary_mark = 0
            summary_mark += row["mark"]

            the_message += f'\n<b>{row["subject"]} </b> \n  {row["comment"]} :   <b>{row["mark"]}</b> \n'
            subject_names.append((row["subject"]))
    the_message += f'Оцінка в сумі: <b>{summary_mark}</b>\n'
    await bot.send_message(message.chat.id, the_message, parse_mode='HTML')
    await bot.send_message(message.chat.id, text="Ваші оцінки були виведені", reply_markup=types.ReplyKeyboardRemove())

def register_handlers_marks(dp : Dispatcher):
    dp.register_message_handler(announcement_command, lambda message: message.text == "Оцінки")
    dp.register_message_handler(view_marks, state=Form.subject)