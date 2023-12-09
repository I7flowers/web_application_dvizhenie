import psycopg2

conn = psycopg2.connect(dbname="dvizhenie_bu1", user="postgres", password="122333", host="127.0.0.1")
cursor = conn.cursor()


conn.autocommit = True
with conn.cursor() as cursor:
    cursor.execute("CREATE TABLE auto_raschet (kust_ex TEXT, kust_ent TEXT, gen_rating REAL, gp_rating REAL, "
                   "first_stage_rating REAL, second_stage_rating REAL, m_e_rating REAL, ruo_rating REAL, "
                   "comment TEXT, exit_date DATE)")
    cursor.execute(
        "CREATE TABLE enterance (kust TEXT PRIMARY KEY, m_e TEXT, gp INTEGER, ruo INTEGER, snph INTEGER, first_stage "
        "DATE, second_stage DATE)")
    cursor.execute(
        "CREATE TABLE exit_ (kust TEXT PRIMARY KEY, m_e TEXT, gp INTEGER, ruo INTEGER, snph INTEGER, exit_date DATE)")
    cursor.execute(
        "CREATE TABLE final (kust_ex TEXT PRIMARY KEY, m_e_ex TEXT, exit_date DATE, kust_ent TEXT, m_e_ent TEXT, "
        "gen_rating INTEGER, comment TEXT)")
    cursor.execute(
        "CREATE TABLE for_handmade_raschet (kust_ex TEXT, kust_ent TEXT, gen_rating REAL, gp_rating REAL, "
        "first_stage_rating REAL, second_stage_rating REAL, m_e_rating REAL, ruo_rating REAL, comment TEXT, "
        "exit_date DATE)")
    cursor.execute(
        "CREATE TABLE raschet (kust_ex TEXT, kust_ent TEXT, gen_rating REAL, gp_rating REAL, first_stage_rating REAL, "
        "second_stage_rating REAL, m_e_rating REAL, ruo_rating REAL, comment TEXT, exit_date DATE)")
    cursor.execute("CREATE TABLE distance (meme TEXT, distance REAL)")


f = open("rrr.txt", "r", encoding="utf8")
s = f.read().split()
f.close()

d = []
for elem in s:
    k = elem.split(",")
    d.append(k)
for elem in d:
    values = (elem[0], elem[1])
    conn.autocommit = True
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO distance VALUES(%s, %s)", values)
