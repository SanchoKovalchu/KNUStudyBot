# Использовать ваш утилитарный модуль.
import myconnutils
import telebot
# import pymysql.cursors
# import mysql.connector
# import pymysql
connection = myconnutils.getConnection()
print ("Connect successful!")

bot = telebot.TeleBot("5302840148:AAGtGfjfQZWbwRn0mqPrv_rEqRhK9XEiarg")
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привіт!')
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    cursor = connection.cursor()
    user_id = message.from_user.id
    if message.text.lower() == 'привіт':
        bot.send_message(message.chat.id, 'Ваші дані:')
        sql = "SELECT * FROM MySQLTestForBot WHERE user_id = %s"
        # Выполнить sql и передать 1 параметр.
        cursor.execute(sql, user_id)
        for row in cursor:
            bot.send_message(message.chat.id,
                             "Ваше ім'я:\t" + str(row["first_name"]) + "\nВаше Прізвище: " + row["last_name"])
    if message.text.lower() == 'вставити':
        sql = "INSERT INTO MySQLTestForBot (user_id, first_name, last_name) " \
              + " VALUES (%s, %s, %s) "
        # Выполнить sql и передать 3 параметра.
        first_name = "Sancho"
        last_name = "Kovalchuk"
        cursor.execute(sql, (user_id, first_name, last_name))
        connection.commit()
        bot.send_message(message.chat.id,
                         "ВСТАВЛЕНО!\nВаше ім'я:\t" + first_name + "\nВаше Прізвище: " + last_name)
    if message.text.lower() == 'оновити':
        first_name = "Sancho2"
        last_name = "Kovalchuk2"
        sql = "UPDATE MySQLTestForBot SET first_name = %s, last_name = %s WHERE user_id = %s"
        # Выполнить sql и передать 3 параметра.
        cursor.execute(sql, (first_name, last_name, user_id))
        connection.commit()
        bot.send_message(message.chat.id,
                         "ОНОВЛЕНО!\nВаше ім'я:\t" + first_name + "\nВаше Прізвище: " + last_name)
    if message.text.lower() == 'видалити':
        sql = "DELETE FROM MySQLTestForBot WHERE user_id = %s"
        # Выполнить sql и передать 3 параметра.
        cursor.execute(sql, user_id)
        connection.commit()
        bot.send_message(message.chat.id,
                         "Видалено!")


if __name__ == '__main__':
    bot.infinity_polling()