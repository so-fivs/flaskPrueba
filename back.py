from flask import Flask, jsonify, request
import pymysql
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Parámetros de conexión a la base de datos
DB_USERNAME = 'sofi'
DB_PASSWORD = ''
DB_HOST = '172.31.27.142'
DB_NAME = 'paginaParcialBigdata'

def get_db_connection():
    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USERNAME,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    return connection

# Ruta para obtener todos los usuarios
@app.route('api/usuarios', methods=['GET'])
def obtener_usuarios():
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, nombre, email, fecha_creacion FROM usuarios")
            usuarios = cursor.fetchall()
        connection.close()
        return jsonify(usuarios), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Ruta para crear un nuevo usuario
@app.route('api/login', methods=['POST'])
def crear_usuario():
    data = request.json
    nombre = data.get('nombre')
    email = data.get('email')
    contraseña = data.get('contraseña')

    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO usuarios (nombre, email, contraseña, fecha_creacion) VALUES (%s, %s, %s, NOW())", (nombre, email, contraseña))
            connection.commit()
        connection.close()
        return jsonify({"message": "Usuario creado con éxito"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Ruta para hacer login (verificar usuario)
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    contraseña = data.get('contraseña')

    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM usuarios WHERE email=%s AND contraseña=%s", (email, contraseña))
            usuario = cursor.fetchone()
        connection.close()

        if usuario:
            return jsonify({"message": "Login exitoso", "usuario": usuario}), 200
        else:
            return jsonify({"error": "Credenciales incorrectas"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
