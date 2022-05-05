import json
from bot_create import cursor, connection
import json

aList = ["1", "2", "3"]

res = json.dumps(aList)

print(res)

sql = "SELECT * FROM teachers_tests WHERE test_owner = %s AND test_subject = %s AND test_name = %s"
cursor.execute(sql, (0, "Math", "Тест 1"))