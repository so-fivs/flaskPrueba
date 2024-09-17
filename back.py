from flask import Flask, jsonify, request
import pymysql
from flask_cors import CORS
import bcrypt

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
@app.route('/api/usuarios', methods=['GET'])
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
@app.route('/api/register', methods=['POST'])
def crear_usuario():
    data = request.json
    nombre = data.get('nombre')
    email = data.get('email')
    contraseña = data.get('contraseña')

    if not nombre or not email or not contraseña:
        return jsonify({"error": "Todos los campos son requeridos"}), 400

    # Hash de la contraseña usando bcrypt
    hashed_password = bcrypt.hashpw(contraseña.encode('utf-8'), bcrypt.gensalt())

    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO usuarios (nombre, email, contraseña, fecha_creacion) VALUES (%s, %s, %s, NOW())",
                (nombre, email, hashed_password.decode('utf-8'))
            )
            connection.commit()
        connection.close()
        return jsonify({"message": "Usuario creado con éxito"}), 201
    except Exception as e:
        return jsonify({"error": f"Error al crear usuario: {str(e)}"}), 500

# Ruta para hacer login (verificar usuario con y sin bcrypt)
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    contraseña = data.get('contraseña')

    if not email or not contraseña:
        return jsonify({"error": "Email y contraseña son requeridos"}), 400

    try:
        connection = get_db_connection()
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("SELECT contraseña FROM usuarios WHERE email=%s", (email,))
            usuario = cursor.fetchone()
        connection.close()

        if usuario:
            stored_password = usuario['contraseña']

            # Si la contraseña almacenada es un hash bcrypt, usar bcrypt para verificar
            if stored_password.startswith("$2b$") or stored_password.startswith("$2a$"):
                if bcrypt.checkpw(contraseña.encode('utf-8'), stored_password.encode('utf-8')):
                    return jsonify({"message": "Login exitoso"}), 200
                else:
                    return jsonify({"error": "Credenciales incorrectas"}), 401
            else:
                # Verificar con texto plano para usuarios antiguos
                if contraseña == stored_password:
                    return jsonify({"message": "Login exitoso"}), 200
                else:
                    return jsonify({"error": "Credenciales incorrectas"}), 401
        else:
            return jsonify({"error": "Credenciales incorrectas"}), 401
    except Exception as e:
        return jsonify({"error": f"Error al hacer login: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
