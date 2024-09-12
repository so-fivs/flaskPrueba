import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_get_usuarios(client):
    response = client.get('/api/usuarios')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_login_success(client):
    response = client.post('/api/login', json={'email': 'test@example.com', 'password': 'password123'})
    assert response.status_code == 200
    assert response.json['mensaje'] == 'Inicio de sesión exitoso'

def test_login_fail(client):
    response = client.post('/api/login', json={'email': 'wrong@example.com', 'password': 'wrongpassword'})
    assert response.status_code == 401
    assert 'error' in response.json
