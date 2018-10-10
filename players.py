from flask import Flask
from flaskext.mysql import MySQL
from flask import jsonify

app = Flask(__name__)

mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'root'
# app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'players'
mysql.init_app(app)
conn = mysql.connect()
cursor = conn.cursor()

@app.route("/", methods=['GET'])
def hello():
    return "Hello"


@app.route("/players", methods=["GET"])
def get_player():
    query = cursor.execute("SELECT * FROM Player_Info")
    return jsonify(cursor.fetchall())

@app.route("/players/<id>", methods=["GET"])
def player_info(id):
    query = cursor.execute("SELECT * FROM Player_Info WHERE id=" + id)
    allPlayer = jsonify(cursor.fetchone())

    return allPlayer

@app.route("/players/<id>/<name>/<position>", methods=["PUT"])
def player_update(id, name, position):
    sql = 'UPDATE Player_Info SET name = %s, position = %s WHERE id=%s'
    val = (str(name), str(position), int(id))
    cursor.execute(sql, val)

@app.route('/players/<name>/<position>', methods=['POST'])
def addNewPlayer(name, position):
    sql = "INSERT INTO Player_Info VALUES (NULL, %s, %s)"
    val = (str(name), str(position))
    cursor.execute(sql, val)

@app.route("/players/<id>", methods=["DELETE"])
def player_delete(id):
    query = cursor.execute("DELETE FROM Player_Info WHERE id=" + id)


if __name__ == '__main__':
    app.run(debug=True)
