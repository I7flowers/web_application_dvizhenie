import datetime

import psycopg2

from dvizhenie.BD_connection import host, user, password, db_name, port


def handmade_raschet():
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name,
        port=port
    )
    connection.autocommit = True
    with connection.cursor() as cursor:
        # выбираем кусты котрые выходят в следующие 45 суток
        today_and_45 = datetime.date.today()+datetime.timedelta(45)

        cursor.execute("SELECT * FROM raschet WHERE exit_date<=%s ORDER BY exit_date, kust_ex", (today_and_45, ))
        for_handmade = cursor.fetchall()
        for elem in for_handmade:
            cursor.execute("INSERT INTO for_handmade_raschet VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", elem)
        cursor.execute("DELETE FROM raschet WHERE exit_date<=%s", (today_and_45, ))


def auto_raschet():
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name,
        port=port
    )
    connection.autocommit = True
    with connection.cursor() as cursor:
        cursor.execute("SELECT DISTINCT kust_ex FROM raschet")
        for kust_ex in cursor.fetchall():
            cursor.execute("SELECT max(gen_rating) FROM raschet WHERE kust_ex=%s", kust_ex)
            max_gen_rating = str(cursor.fetchone()[0])
            if max_gen_rating == 'None':
                cursor.execute("INSERT INTO final(kust_ex, kust_ent, m_e_ent, gen_rating, comment) VALUES(%s, %s, %s, "
                               "%s, %s)",(kust_ex[0], 'нет кандидата', '', 0, ''))
            else:
                values = (kust_ex[0], max_gen_rating)
                cursor.execute("SELECT kust_ex, kust_ent, GEN_rating, comment FROM raschet WHERE kust_ex=%s AND "
                               "GEN_rating=%s ORDER BY exit_date, kust_ex",
                               values)
                finish_solution = cursor.fetchone()
                cursor.execute("DELETE FROM raschet WHERE kust_ent=%s", (finish_solution[1],))
                cursor.execute("INSERT INTO final(kust_ex, kust_ent, GEN_rating, comment) VALUES(%s, %s, %s, %s)",
                               finish_solution)
        cursor.execute("SELECT * FROM final")
        for elem in cursor.fetchall():
            kust_ex = elem[0]
            kust_ent = elem[3]
            cursor.execute("SELECT m_e, exit_date FROM exit_ WHERE kust = %s", (kust_ex,))
            m_e_ex_exit_date = cursor.fetchall()[0]
            m_e_ex = m_e_ex_exit_date[0]
            exit_date = m_e_ex_exit_date[1]
            cursor.execute("UPDATE final SET m_e_ex = %s, exit_date =%s WHERE kust_ex = %s", (m_e_ex, exit_date, kust_ex))
            if kust_ent == "нет кандидата":
                continue
            else:
                cursor.execute("SELECT m_e FROM enterance WHERE kust = %s", (kust_ent,))
                m_e_ent = cursor.fetchone()
                cursor.execute("UPDATE final SET m_e_ent = %s WHERE kust_ent = %s", (m_e_ent[0], kust_ent))
    connection.close()
