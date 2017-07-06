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
    g.request_time = lambda : ((time.time() - g.request_start_time) * 1000)

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
        calo_from = request.form['cal_from']
        calo_to = request.form['cal_to']

        ing_name =[]
        dish_dict = {}
        # sql_query = 'SELECT * FROM food_data WHERE Ingredients LIKE "%{}%"'.format(ingredient)

        sql_query = 'SELECT * FROM food_data WHERE Cal BETWEEN {} AND {}'.format(calo_from,calo_to)

        # if course_num != "":
        #     sql_query = 'select * from class_data where CourseNum=' + course_num
        # else:
        #     sql_query = "select * from class_data where Instructor='" +  inst + "'"

        # table_info = "<tr> <th> ID </th> <th> Name </th> <th> Type </th>  <th> Ingredients </th></tr>"
        q_time_start = time.time()
        con = create_connection()
        cur = con.cursor()
        cur.execute(sql_query)
        results = []
        for result in cur.fetchall():
            dishId = result[0] # Dish ID
            name = result[1] # Name of the Dish
            type = result[2] # Type of the Dish
            cal = result[5] # Dish Ingredient

            # table_info += "<tr><td> {} </td> <td> {} </td> <td> {} </td> <td> {} </td></tr>".format(dishId,name,type,ingre)
            name += ".jpg"
            ing_name.append(name)
            dish_dict[name]= [type,cal]
            print(result)
            results.append(result)

        q_time_end = time.time()
        q_full_time = (q_time_end - q_time_start) * 1000
        t = request.values.get('t', 0)
        time.sleep(float(t))


        num_of_pictures = len(results)

        return render_template('query_one.html', resultinfo=results, q_time=q_full_time,ing_name=dish_dict,num_pic=num_of_pictures)

@app.route('/query2', methods=['GET','POST'])
def view_con():
    if request.method == 'GET':
        t = request.values.get('t', 0)
        time.sleep(float(t))

        return render_template("query_two.html")
    elif request.method == 'POST':
        calo_from = request.form['cal_great']
        ingredient = request.form['ingredient']

        ing_name =[]
        dish_dict = {}
        # sql_query = 'SELECT * FROM food_data WHERE Ingredients LIKE "%{}%"'.format(ingredient)

        #sql_query = 'SELECT * FROM food_data WHERE Cal BETWEEN {} AND {}'.format(calo_from,calo_to)

        sql_query = 'SELECT * FROM food_data WHERE Cal >= {} AND Ingredients LIKE "%{}%"'.format(calo_from,ingredient)

        # if course_num != "":
        #     sql_query = 'select * from class_data where CourseNum=' + course_num
        # else:
        #     sql_query = "select * from class_data where Instructor='" +  inst + "'"

        # table_info = "<tr> <th> ID </th> <th> Name </th> <th> Type </th>  <th> Ingredients </th></tr>"
        q_time_start = time.time()
        con = create_connection()
        cur = con.cursor()
        cur.execute(sql_query)
        results = []
        for result in cur.fetchall():
            dishId = result[0] # Dish ID
            name = result[1] # Name of the Dish
            type = result[2] # Type of the Dish
            cal = result[5] # Dish Ingredient

            # table_info += "<tr><td> {} </td> <td> {} </td> <td> {} </td> <td> {} </td></tr>".format(dishId,name,type,ingre)
            name += ".jpg"
            ing_name.append(name)
            dish_dict[name]= [type,cal]
            print(result)
            results.append(result)

        q_time_end = time.time()
        q_full_time = (q_time_end - q_time_start) * 1000
        t = request.values.get('t', 0)
        time.sleep(float(t))


        num_of_pictures = len(results)

        return render_template('query_two.html', resultinfo=results, q_time=q_full_time,ing_name=dish_dict,num_pic=num_of_pictures)


@app.route('/topIng', methods=['GET'])
def view_ing_page():
    return render_template("top_que.html")

@app.route('/topIng',methods=['POST'])
def view_top_ing():
    ing_query = "SELECT Ingredients FROM food_data"

    con = create_connection()
    cur = con.cursor()
    cur.execute(ing_query)

    ing_res = []
    for ingres in cur.fetchall():
        print(ingres)

    return render_template("top_que.html")

if __name__ == '__main__':
    app.run(debug=True)