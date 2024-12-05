from flask import Flask,request
import sqlite3

app = Flask(__name__)

conn = sqlite3.connect("cars.db")
conn.execute("CREATE TABLE IF NOT EXISTS cars (id INTEGER PRIMARY KEY, brand TEXT, model TEXT, year INTEGER)")
conn.close()


@app.route('/')
def index():
    conn = sqlite3.connect("cars.db")
    cars = conn.execute("SELECT * FROM cars").fetchall()
    conn.close()

    car_list = "<h1>Список автомобілей</h1>"
    for car in cars:
        car_list += f"{car[1]} {car[2]} ({car[3]}) - <a href='/delete/{car[0]}'>Видалити</a><br>"
    car_list += "<br><a href='/add'>Додати автомобиль</a>"
    return car_list


@app.route('/add')
def add_car():
    return '''
        <h1>Додати автомобиль</h1>
        <form action="/add_car" method="get">
            Марка: <input type="text" name="brand"><br>
            Модель: <input type="text" name="model"><br>
            Рік: <input type="number" name="year"><br>
            <input type="submit" value="Додати">
        </form>
    '''


@app.route('/add_car')
def add_car_process():
    brand = request.args.get('brand')
    model = request.args.get('model')
    year = request.args.get('year')

    conn = sqlite3.connect("cars.db")
    conn.execute("INSERT INTO cars (brand, model, year) VALUES (?, ?, ?)", (brand, model, year))
    conn.commit()
    conn.close()

    return '''
        <h1>Автомобіль доданий!</h1>
        <a href="/">Назад до списку автомобілей</a>
    '''


@app.route('/delete/<int:car_id>')
def delete_car(car_id):
    conn = sqlite3.connect("cars.db")
    conn.execute("DELETE FROM cars WHERE id = ?", (car_id,))
    conn.commit()
    conn.close()

    return '''
        <h1>Автомобіль видалений!</h1>
        <a href="/">Назад до списку автомобілей</a>
    '''


if __name__ == '__main__':
    app.run(debug=True)
