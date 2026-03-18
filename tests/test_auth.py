import unittest
import json
import os
from app import create_app
from app.extensions import db

class JWTAuthTestCase(unittest.TestCase):
    def setUp(self):
        # Configuramos la DB en memoria para pruebas rápidas
        os.environ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = create_app('test')
        self.app.config['JWT_COOKIE_CSRF_PROTECT'] = False # Disable during tests to simplify client mocking
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_register_and_login(self):
        # 1. Registrar usuario
        res = self.client.post('/api/auth/register', json={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123'
        })
        self.assertEqual(res.status_code, 201)

        # 2. Login de usuario
        res = self.client.post('/api/auth/login', json={
            'username': 'testuser',
            'password': 'password123'
        })
        self.assertEqual(res.status_code, 200)
        
        # Guardaremos las cookies que devuelva el login
        cookies = res.headers.getlist('Set-Cookie')
        access_cookie_present = any('access_token_cookie' in c for c in cookies)
        refresh_cookie_present = any('refresh_token_cookie' in c for c in cookies)
        
        self.assertTrue(access_cookie_present)
        self.assertTrue(refresh_cookie_present)

    def test_protected_route_without_token(self):
        res = self.client.get('/protected')
        self.assertEqual(res.status_code, 401) # Unauthorized

    def test_protected_route_with_token(self):
        # Registramos y logueamos primero para tener las cookies
        self.client.post('/api/auth/register', json={
            'username': 'testuser', 'email': 'test@example.com', 'password': 'password123'
        })
        login_res = self.client.post('/api/auth/login', json={
            'username': 'testuser', 'password': 'password123'
        })
        
        # Extraemos las cookies del Set-Cookie header general y las ponemos en el test client local
        for cookie_string in login_res.headers.getlist('Set-Cookie'):
            # Formato de cookie devuelto es "name=value; Path=/; ..."
            # Sacamos el par key=value
            key_val = cookie_string.split(';')[0]
            key, val = key_val.split('=', 1)
            self.client.set_cookie(key, val)

        # Llamamos la ruta protegida que requiere un Refresh token válido en cookies
        res = self.client.get('/protected')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data['user'], 'testuser')

    def test_logout(self):
        # Registrar y login
        self.client.post('/api/auth/register', json={
            'username': 'testuser', 'email': 'test@test.com', 'password': '123'
        })
        login_res = self.client.post('/api/auth/login', json={
            'username': 'testuser', 'password': '123'
        })
        
        for cookie_string in login_res.headers.getlist('Set-Cookie'):
            key, val = cookie_string.split(';')[0].split('=', 1)
            self.client.set_cookie(key, val)
            
        # Logout explícito (revoca el access token en blocklist)
        res_logout = self.client.post('/api/auth/logout')
        self.assertEqual(res_logout.status_code, 200)
        
        # Al intentar acceder de nuevo a una ruta protegida con el mismo cliente/cookies DEBE RECHAZARLO
        res_protected = self.client.get('/protected')
        self.assertEqual(res_protected.status_code, 401)

if __name__ == '__main__':
    unittest.main()
