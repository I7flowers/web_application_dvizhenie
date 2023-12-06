from flask import Flask, render_template, url_for, request, flash, redirect

import psycopg2
import psycopg2.extras
from dvizhenie1.starting import main, final

app = Flask(__name__)
app.secret_key = '122333'

DB_HOST = "127.0.0.1"
DB_USER = "postgres"
DB_PASS = "122333"
DB_NAME = "dvizhenie_BU"

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)


@app.route('/')
def index():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    s = "SELECT * FROM final"
    cur.execute(s)
    list_final = cur.fetchall()
    return render_template("index.html", list_final=list_final)


@app.route('/BY_inf')
def BY_inf():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    s = "SELECT * FROM exit_"
    cur.execute(s)
    list_BY = cur.fetchall()
    return render_template("BY_inf.html", list_BY=list_BY)


@app.route('/add_BY', methods=['POST'])
def add_BY():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        kust = request.form['kust']
        m_e = request.form['m_e']
        exit_date = request.form['exit_date']
        gp = request.form['gp']
        ruo = request.form['ruo']
        snph = request.form['snph']
        cur.execute('SELECT(EXISTS(SELECT kust FROM exit_ WHERE kust=%s))', (kust,))
        kust_exists = cur.fetchone()[0]
        if kust_exists:
            flash('Такой куст уже есть в списке!', 'error')
        elif m_e == 'error' or gp == 'error' or ruo == 'error' or snph == 'error':
            print('туту')
            flash('Внесите корректные данные!', 'error')

        else:
            cur.execute('INSERT INTO exit_(kust, m_e, exit_date, GP, RUO, SNPH) VALUES (%s, %s, %s, %s, %s, %s)',
                        (kust, m_e, exit_date, gp, ruo, snph))
            flash('Информация успешно добавлена', 'success')
        conn.commit()
        return redirect(url_for('BY_inf'))


@app.route('/BY_inf/edit/<kust>', methods=['POST', 'GET'])
def edit_BY(kust):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT * FROM exit_ WHERE kust=%s', (kust,))
    data = cur.fetchall()
    cur.close()
    return render_template('edit_BY.html', BY=data[0])


@app.route('/BY_inf/update/<kust>', methods=['POST'])
def update_BY():
    if request.method == 'POST':
        kust = request.form['kust']
        m_e = request.form['m_e']
        exit_date = request.form['exit_date']
        gp = request.form['gp']
        ruo = request.form['ruo']
        snph = request.form['snph']
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute('UPDATE exit_ SET m_e=%s, exit_date=%s, GP=%s, RUO=%s, SNPH=%s WHERE kust=%s',
                    (m_e, exit_date, gp, ruo, snph, kust))
        flash('Информация обновлена', 'success')
        conn.commit()
        return redirect(url_for('BY_inf'))


@app.route('/BY_inf/delete/<string:kust>', methods=['POST', 'GET'])
def delete_BY(kust):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT * FROM exit_ WHERE kust=%s', (kust,))
    data = cur.fetchall()[0]
    cur.execute('DELETE FROM exit_ WHERE kust=%s', (data[0],))
    flash('Куст удален', 'success')
    conn.commit()
    return redirect(url_for('BY_inf'))


@app.route('/KP_inf')
def KP_inf():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    s = "SELECT * FROM enterance"
    cur.execute(s)
    list_KP = cur.fetchall()
    return render_template("KP_inf.html", list_KP=list_KP)


@app.route('/add_KP', methods=['POST'])
def add_KP():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        kust = request.form['kust']
        m_e = request.form['m_e']
        first_stage = request.form['first_stage']
        second_stage = request.form['second_stage']
        gp = request.form['gp']
        ruo = request.form['ruo']
        snph = request.form['snph']
        cur.execute('SELECT(EXISTS(SELECT kust FROM enterance WHERE kust=%s))', (kust,))
        kust_exists = cur.fetchone()[0]
        if kust_exists:
            flash('Такой куст уже есть в списке!', 'error')
        elif m_e == 'error' or gp == 'error' or ruo == 'error' or snph == 'error':
            flash('Внесите корректные данные!', 'error')
        else:
            cur.execute('INSERT INTO enterance(kust, m_e, first_stage, second_stage, GP, RUO, SNPH) VALUES (%s, %s, '
                        '%s, %s, %s, %s, %s)', (kust, m_e, first_stage, second_stage, gp, ruo, snph))
            flash('Информация успешно добавлена', 'success')
        conn.commit()
        return redirect(url_for('KP_inf'))


@app.route('/KP_inf/edit/<kust>', methods=['POST', 'GET'])
def edit_KP(kust):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT * FROM enterance WHERE kust=%s', (kust,))
    data = cur.fetchall()
    cur.close()
    return render_template('edit_KP.html', KP=data[0])


@app.route('/KP_inf/update/<kust>', methods=['POST'])
def update_kust():
    if request.method == 'POST':
        kust = request.form['kust']
        m_e = request.form['m_e']
        first_stage = request.form['first_stage']
        second_stage = request.form['second_stage']
        gp = request.form['gp']
        ruo = request.form['ruo']
        snph = request.form['snph']
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(
            'UPDATE ENTERANCE SET m_e=%s, first_stage=%s, second_stage=%s, GP=%s, RUO=%s, SNPH=%s WHERE kust=%s',
            (m_e, first_stage, second_stage, gp, ruo, snph, kust))
        flash('Информация обновлена', 'success')
        conn.commit()
        return redirect(url_for('KP_inf'))


@app.route('/KP_inf/delete/<string:kust>', methods=['POST', 'GET'])
def delete_kust(kust):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT * FROM enterance WHERE kust=%s', (kust,))
    data = cur.fetchall()[0]
    cur.execute('DELETE FROM enterance WHERE kust=%s', (data[0],))
    flash('Куст удален', 'success')
    conn.commit()
    return redirect(url_for('KP_inf'))


@app.route('/handmade_raschet')
def handmade_raschet():
    main()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    s = "SELECT * FROM for_handmade_raschet"
    cur.execute(s)
    list_for_handmade_raschet = cur.fetchall()
    return render_template("handmade_raschet.html", list_for_handmade_raschet=list_for_handmade_raschet)


@app.route('/handmade_raschet1')
def handmade_raschet1():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    s = "SELECT * FROM for_handmade_raschet"
    cur.execute(s)
    list_for_handmade_raschet = cur.fetchall()
    return render_template("handmade_raschet.html", list_for_handmade_raschet=list_for_handmade_raschet)


@app.route('/handmade_raschet/commit/<string:kust_ex>/<string:kust_ent>', methods=['POST', 'GET'])
def commit(kust_ex, kust_ent):
    print(kust_ex, kust_ent)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT * FROM for_handmade_raschet WHERE kust_ex=%s AND kust_ent=%s', (kust_ex, kust_ent))
    data = cur.fetchone()
    cur.execute('INSERT INTO final(kust_ex, exit_date, kust_ent, gen_rating, comment) VALUES (%s, %s, %s, %s, %s)',
                (data[0], data[9], data[1], data[2], data[8]))
    cur.execute('DELETE FROM for_handmade_raschet WHERE kust_ex=%s OR kust_ent=%s', (data[0], data[1]))
    conn.commit()
    return redirect(url_for('handmade_raschet1'))


@app.route('/index_after_raschet')
def index_auto_raschet():
    final()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    s = "SELECT * FROM final"
    cur.execute(s)
    list_final = cur.fetchall()
    return render_template("index.html", list_final=list_final)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
