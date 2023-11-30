from flask import Flask, render_template, url_for, request, flash, redirect
import psycopg2
import psycopg2.extras

app = Flask(__name__)
app.secret_key = '122333'

DB_HOST = "127.0.0.1"
DB_USER = "postgres"
DB_PASS = "122333"
DB_NAME = "dvizhenie_BU"

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)


@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


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
        GP = request.form['GP']
        RUO = request.form['RUO']
        SNPH = request.form['SNPH']
        cur.execute('INSERT INTO exit_(kust, m_e, exit_date, GP, RUO, SNPH) VALUES (%s, %s, %s, %s, %s, %s)',
                    (kust, m_e, exit_date, GP, RUO, SNPH))
        conn.commit()
        flash('Информация успешно добавлена')
        return redirect(url_for('BY_inf'))


@app.route('/BY_inf/edit/<kust>', methods=['POST', 'GET'])
def edit_BY(kust):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT * FROM exit_ WHERE kust=%s', (kust,))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit_BY.html', BY=data[0])


@app.route('/BY_inf/update/<kust>', methods=['POST'])
def update_BY(kust):
    if request.method == 'POST':
        kust = request.form['kust']
        m_e = request.form['m_e']
        exit_date = request.form['exit_date']
        GP = request.form['GP']
        RUO = request.form['RUO']
        SNPH = request.form['SNPH']
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute('UPDATE exit_ SET m_e=%s, exit_date=%s, GP=%s, RUO=%s, SNPH=%s WHERE kust=%s',(m_e, exit_date, GP, RUO, SNPH, kust))
        flash('Информация обновлена')
        conn.commit()
        return redirect(url_for('BY_inf'))


@app.route('/BY_inf/delete/<string:kust>', methods=['POST', 'GET'])
def delete_BY(kust):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT * FROM exit_ WHERE kust=%s', (kust,))
    data = cur.fetchall()[0]
    print(data[0])
    cur.execute('DELETE FROM exit_ WHERE kust=%s', (data[0],))
    flash('Куст удален')
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
        GP = request.form['GP']
        RUO = request.form['RUO']
        SNPH = request.form['SNPH']
        cur.execute('INSERT INTO enterance(kust, m_e, first_stage, second_stage, GP, RUO, SNPH) VALUES (%s, %s, %s, %s, %s, %s, %s)',
                    (kust, m_e, first_stage, second_stage, GP, RUO, SNPH))
        conn.commit()
        flash('Информация успешно добавлена')
        return redirect(url_for('KP_inf'))


@app.route('/KP_inf/edit/<kust>', methods=['POST', 'GET'])
def edit_KP(kust):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT * FROM enterance WHERE kust=%s', (kust,))
    data = cur.fetchall()
    cur.close()
    return render_template('edit_KP.html', KP=data[0])


@app.route('/KP_inf/update/<kust>', methods=['POST'])
def update_kust(kust):
    if request.method == 'POST':
        kust = request.form['kust']
        m_e = request.form['m_e']
        first_stage = request.form['first_stage']
        second_stage = request.form['second_stage']
        GP = request.form['GP']
        RUO = request.form['RUO']
        SNPH = request.form['SNPH']
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute('UPDATE ENTERANCE SET m_e=%s, first_stage=%s, second_stage=%s, GP=%s, RUO=%s, SNPH=%s WHERE kust=%s',(m_e, first_stage, second_stage, GP, RUO, SNPH, kust))
        flash('Информация обновлена')
        conn.commit()
        return redirect(url_for('KP_inf'))


@app.route('/KP_inf/delete/<string:kust>', methods=['POST', 'GET'])
def delete_kust(kust):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT * FROM enterance WHERE kust=%s', (kust,))
    data = cur.fetchall()[0]
    cur.execute('DELETE FROM enterance WHERE kust=%s', (data[0],))
    flash('Куст удален')
    conn.commit()
    return redirect(url_for('KP_inf'))


@app.route('/handmade_raschet')
def handmade_raschet():
    return render_template("handmade_raschet.html")


@app.route('/bd')
def bd():
    return render_template("for_bd.html")


if __name__ == "__main__":
    app.run(debug=True)