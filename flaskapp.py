from flask import Flask, render_template, url_for, request, g
import time
import sqlite3
import pandas as pd
import os

app = Flask(__name__)


def create_connection():
    return sqlite3.connect(os.path.join(app.root_path, 'static', 'class.db'))


def create_db():
    con = create_connection()
    cur = con.cursor()
    cur.execute('select count(*) from class_data')
    (row_count,) = cur.fetchone()
    if row_count > 0:
        print('Table exists')
        cur.close()
        con.close()
    else:
        df = pd.read_csv(os.path.join(app.root_path, 'dataset','Classes.csv'))
        df.to_sql('class_data', con, if_exists='replace', index=False)
        con.commit()
        con.close()

create_db()

@app.before_request
def before_request():
    g.request_start_time = time.time()
    g.request_time = lambda : "%.5f ms" % ((time.time() - g.request_start_time) * 1000)


@app.route('/', methods=['GET','POST'])
def view_contents():
    if request.method == 'GET':
        t = request.values.get('t', 0)
        time.sleep(float(t))  # just to show it works...
        return render_template("query_one.html")
    elif request.method == 'POST':
        course_num = request.form['course']
        inst = request.form['instructor']

        sql_query = ""

        if course_num != "":
            sql_query = 'select * from class_data where CourseNum=' + course_num
        else:
            sql_query = "select * from class_data where Instructor='" +  inst + "'"

        con = create_connection()
        cur = con.cursor()
        cur.execute(sql_query)
        results = []
        for result in cur.fetchall():
            results.append(result)

        t = request.values.get('t', 0)
        time.sleep(float(t))  # just to show it works...
        return render_template('query_one.html', resultinfo=results)


if __name__ == '__main__':
    app.run()