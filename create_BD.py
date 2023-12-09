import psycopg2

conn = psycopg2.connect(
    host="127.0.0.1",
    user="postgres",
    password="122333",
    database="postgres")

cursor = conn.cursor()

conn.autocommit = True
# команда для создания базы данных metanit
sql = "CREATE DATABASE dvizhenie_bu1"

# выполняем код sql
cursor.execute(sql)
print("База данных успешно создана")

cursor.close()
conn.close()
