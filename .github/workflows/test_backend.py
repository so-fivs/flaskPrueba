import pytest
import json
from app import app, get_db_connection

@pytest.fixture
def client():
    # Cambiar la configuración de la base de datos para la prueba
    app.config['TESTING'] = True
    app.config['DB_NAME'] = 'paginaParcialBigdata_test'  # Usar base de datos de prueba

    with app.test_client() as client:
        yield client

def test_obtener_usuarios(client):
    response = client.get('/api/usuarios')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_crear_usuario(client):
    nuevo_usuario = {
        "nombre": "Prueba",
        "email": "prueba@example.com",
        "contraseña": "password123"
    }
    response = client.post('/api/register', data=json.dumps(nuevo_usuario), content_type='application/json')
    assert response.status_code == 201
    assert response.json['message'] == "Usuario creado con éxito"

def test_login_usuario(client):
    login_data = {
        "email": "prueba@example.com",
        "contraseña": "password123"
    }
    response = client.post('/api/login', data=json.dumps(login_data), content_type='application/json')
    assert response.status_code == 200
    assert response.json['message'] == "Login exitoso"
