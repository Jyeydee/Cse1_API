from flask import Flask, make_response, jsonify, request
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "cardatabase"

app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


def data_fetch(query):
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    return data


@app.route("/cars", methods=["GET"])
def get_actors():
    data = data_fetch("""select * from cars""")
    return make_response(jsonify(data), 200)


@app.route("/cars/<int:id>", methods=["GET"])
def get_actor_by_id(id):
    data = data_fetch("""SELECT * FROM cars where car_id = {}""".format(id))
    return make_response(jsonify(data), 200)

@app.route("/carAdd", methods=["GET", "POST"])
def add_car():
    
    conn = mysql.connection.cursor()
    info = request.get_json()

    carid = info['car_id']
    car_year = info['car_year_of_manufacture']
    car_model = info['model']
    make_id = info['manufacturer_id']


    query = """INSERT INTO `cardatabase`.`cars` (`car_id`, `car_year_of_manufacture`, `model`, `manufacturer_id`) 
               VALUES (%s, %s, %s, %s)"""

    values = (carid, car_year, car_model, make_id)
    conn.execute(query, values)

    mysql.connection.commit()
    rows_added = conn.rowcount
    print(f"Rows ADDED: {rows_added}")
    conn.close()

    return make_response(jsonify({"message": "Added Successfully", "row_added": rows_added}), 200)

if __name__ == "__main__":
    app.run(debug=True)
