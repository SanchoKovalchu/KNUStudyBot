from bot_create import cursor, bot
from aiogram import types, Dispatcher


async def sql_read_photo(message : types.Message):
    sql = "SELECT * FROM file_storage"
    cursor.execute(sql)
    for row in cursor.fetchall():
        if row["file_type"] == 'photo':
            await bot.send_photo(message.chat.id, row["file_id"], caption=  f'Назва: {row["name"]}\nОпис: {row["description"]}')
        elif row["file_type"] == 'video':
            await bot.send_video(message.chat.id, row["file_id"], caption= f'Назва: {row["name"]}\nОпис: {row["description"]}')
        elif row["file_type"] == 'audio':
            await bot.send_audio(message.chat.id, row["file_id"], caption=  f'Назва: {row["name"]}\nОпис: {row["description"]}')
        elif row["file_type"] == 'voice':
            await bot.send_voice(message.chat.id, row["file_id"], caption=  f'Назва: {row["name"]}\nОпис: {row["description"]}')
        elif row["file_type"] == 'animation':
            await bot.send_animation(message.chat.id, row["file_id"], caption=  f'Назва: {row["name"]}\nОпис: {row["description"]}')
        elif row["file_type"] == 'video_note':
            await bot.send_video_note(message.chat.id, row["file_id"], caption=  f'Назва: {row["name"]}\nОпис: {row["description"]}')
        else:
            await bot.send_document(message.chat.id, row["file_id"], caption=  f'Назва: {row["name"]}\nОпис: {row["description"]}')

def register_handlers_files(dp : Dispatcher):
    dp.register_message_handler(sql_read_photo, lambda message: message.text == "Переглянути матеріал")