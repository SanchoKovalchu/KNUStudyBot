# import pymysql.cursors
# import json
# import schedule
# import time
# from datetime import datetime
# connection = pymysql.connect(host='s2.thehost.com.ua',
#                              user='MySQLBot',
#                              password='MySQLBot1',
#                              db='WeatherTEST',
#                              charset='utf8mb4',
#                              cursorclass=pymysql.cursors.DictCursor)
#
# cursor = connection.cursor()
#
#
# def send_message():
#     print("Get ready!")
#     sql = "SELECT * FROM add_file_storage"
#     cursor.execute(sql)
#     raw_dates_string = []
#     file_id_array = []
#     dates_array_for_comparing = []
#     i = -1
#     for row in cursor:
#         i += 1
#         print(i)
#         raw_dates_string.append(row["date_time"])
#         file_id_array.append(row["file_id"])
#     print(raw_dates_string)
#     print(file_id_array)
#
#     now = datetime.now()
#     dt_string = now.strftime("%d-%m-%Y %H:%M:%S")
#     unixtime = datetime.strptime(str(dt_string), '%d-%m-%Y %H:%M:%S')
#     unixtime_now = time.mktime(unixtime.timetuple())
#     print(unixtime_now)
#     for k in range(len(raw_dates_string)):
#         date_string = raw_dates_string[k].split(', ')
#         dates_array_for_comparing.append(date_string[0])
#         if unixtime_now > float(dates_array_for_comparing[k]):
#             print("YES")
# schedule.every(5).minutes.do(send_message)
# while True:
#     schedule.run_pending()
#     time.sleep(1)
