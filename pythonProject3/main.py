from flask import Flask, render_template, request, url_for, redirect
import pyodbc
app = Flask(__name__)
connection = pyodbc.connect('Driver={SQL Server};'
                      'Server=name server;'
                      'Database=name bd;'
                      )
cursor = connection.cursor()
# словарь запросов на вывод таблиц
queries = {
    'Tour': 'SELECT * FROM Turi;',
    'Sale': 'select ID, TitleSale, ROUND(Size,2) as Size, DateStart, DateEnd   from Sale;',
    'Hostels': 'SELECT  ID, Title, Country, City, TypyFood,ROUND(DistanseAirport,2) as DistanseAirport, ROUND(DistanseBeach,2) as DistanseBeach, ROUND(DistanseSea,2) as DistanseSea, Service, Category, Price from Hotels;',
    'Orders': 'select * from Orders;',
    'Clients': 'SELECT * FROm Clients;',
    'Comments': 'select * from Commets;'
}
users = {
    "GP012": "qwe321w",
    "GP912": "zxc341e"
}
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/bd')
def bd():
    return render_template("BD.html", queries=queries)
@app.route('/bd2')
def bd2():
    return render_template("BD2.html", queries=queries)
###### FLASK SERVER ######
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if username == 'GP012' and users[username] == password:
        return redirect(url_for('bd'))
    elif username == 'GP912' and users[username] == password:
        return redirect(url_for('bd2'))
    else:
        return render_template('index.html')
@app.route('/query', methods=['POST'])
def query():
    table_name = request.form['query']
    query_name = request.form['query']
    cursor = connection.cursor()
    cursor.execute(queries[query_name])
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]  # извлекаем названия столбцов
    return render_template('BD.html', rows=rows, columns=columns), table_name
@app.route('/execute_query', methods=['POST'])
def execute_query():
    sql_query = request.form['sql_query']
    cursor = connection.cursor()
    cursor.execute(sql_query)
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]  # извлекаем названия столбцов
    return render_template('BD.html', rows=rows, columns=columns)
@app.route('/delete_row', methods=['POST'])
def delete_row():
    table_name = request.form['table_name']
    row_id = request.form['row_id']
    sql_query = f"""DELETE FROM {table_name}
                            WHERE ID={row_id};"""
    cursor = connection.cursor()
    cursor.execute(sql_query)
    return render_template('BD.html')
@app.route('/add_assessment', methods=['POST'])
def add_assessment():
    client = request.form['client']
    comment = request.form['comment']
    assessment = int(request.form['assessment'])
    date_com = request.form['date_com']
    cursor.execute('''
    INSERT INTO Commets (Client, Commets, Assessment, DateCom)
    VALUES (?, ?, ?, ?)
    ''', (client, comment, assessment, date_com))
    return redirect(url_for('bd'))
@app.route('/add_assessment1', methods=['POST'])
def add_assessment1():
    surname = request.form['surname']
    name = request.form['name']
    secondname = request.form['secondname']
    pasport = request.form['pasport']
    number = request.form['number']
    email = request.form['email']
    cursor.execute('''
    INSERT INTO Clients (Surename, Name, SecondName, Pasport, Number, Email)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (surname, name, secondname, pasport, number,email))
    return redirect(url_for('bd'))
@app.route('/add_assessment2', methods=['POST'])
def add_assessment2():
    hotel = request.form['hotel']
    titletour = request.form['titletour']
    datestart = request.form['datestart1']
    dateend = request.form['dateend1']
    category = request.form['category']
    price = request.form['price']
    cursor.execute('''
    INSERT INTO Turi (Hotel, TitleTour, DateStart, DateEnd, Category, Price)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (hotel, titletour, datestart, dateend, category, price))
    return redirect(url_for('bd'))
@app.route('/add_assessment3', methods=['POST'])
def add_assessment3():
    titlesale = request.form['titlesale']
    size = request.form['size']
    datestart2 = request.form['datestart2']
    dateend2 = request.form['dateend2']
    cursor.execute('''
    INSERT INTO Sale (TitleSale, Size, DateStart, DateEnd)
    VALUES (?, ?, ?, ?)
    ''', (titlesale, size, datestart2, dateend2))
    return redirect(url_for('bd'))
@app.route('/add_assessment5', methods=['POST'])
def add_assessment4():
    clt = request.form['clt']
    tr = request.form['tr']
    sts = request.form['sts']
    db = request.form['db']
    sl = request.form['sl']
    cursor.execute('''
    INSERT INTO Orders (Client, Tour, Status, DateBron, Sale)
    VALUES (?, ?, ?, ?, ?)
    ''', (clt, tr, sts, db, sl))
    return redirect(url_for('bd'))
@app.route('/opion', methods=['POST'])
def opion():
    sql_query = request.form['procedure']
    cursor.execute(f"EXEC {sql_query};")
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]  # извлекаем названия столбцов
    return render_template('BD.html', rows=rows, columns=columns)
if __name__ == "__main__":
    app.run(debug=True)