from flask import Flask, render_template, url_for, request, g
import time
import sqlite3
import pandas as pd
import os

app = Flask(__name__)


def create_connection():
    return sqlite3.connect(os.path.join(app.root_path, 'static', 'class.db'))


# def create_db():
#     con = create_connection()
#     #cur = con.cursor()
#     #cur.execute('select count(*) from food_data')
#     #(row_count,) = cur.fetchone()
#     #print(row_count)
#     # if row_count > 0:
#     #     print('Table exists')
#     #     cur.close()
#     #     con.close()
#     # else:
#     df = pd.read_csv(os.path.join(app.root_path,'static','dataset','main.csv'))
#     df.to_sql('food_data', con, if_exists='replace', index=False)
#     con.commit()
#     con.close()
#
# create_db()

@app.before_request
def before_request():
    g.request_start_time = time.time()
    g.request_time = lambda : "%.5f ms" % ((time.time() - g.request_start_time) * 1000)

@app.route('/', methods=['GET'])
def view_db():
    return render_template("create_db.html")

@app.route('/', methods=['POST'])
def create_db():
    con = create_connection()
    df = pd.read_csv(os.path.join(app.root_path, 'static', 'dataset', 'main.csv'))
    df.to_sql('food_data', con, if_exists='replace', index=False)
    con.commit()
    con.close()
    resultinfo = "Database Not Created"
    if con:
        resultinfo = "Database Created"
    return render_template("create_db.html",resultinfo=resultinfo)


@app.route('/query1', methods=['GET','POST'])
def view_contents():
    if request.method == 'GET':
        t = request.values.get('t', 0)
        time.sleep(float(t))

        return render_template("query_one.html")
    elif request.method == 'POST':
        ingredient = request.form['ingredient']

        sql_query = 'SELECT * FROM food_data WHERE Ingredients LIKE "%{}%"'.format(ingredient)

        # if course_num != "":
        #     sql_query = 'select * from class_data where CourseNum=' + course_num
        # else:
        #     sql_query = "select * from class_data where Instructor='" +  inst + "'"

        con = create_connection()
        cur = con.cursor()
        cur.execute(sql_query)
        results = []
        for result in cur.fetchall():
            results.append(result)

        t = request.values.get('t', 0)
        time.sleep(float(t))

        return render_template('query_one.html', resultinfo=results)


if __name__ == '__main__':
    app.run()