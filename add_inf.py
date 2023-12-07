import psycopg2

host = "127.0.0.1"
user = "postgres"
password = "122333"
db_name = "dvizhenie_BU"
port = "5432"


connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name,
        port=port)

f = open("rrr.txt", "r", encoding="utf8")
s = f.read().split()
f.close()

d = []
for elem in s:
    k = elem.split(",")
    d.append(k)
print(d)
connection.autocommit = True
with connection.cursor() as cursor:
    for elem in d:
        values = (elem[0], elem[1])
        cursor.execute("INSERT INTO distance VALUES(%s, %s)", values)
