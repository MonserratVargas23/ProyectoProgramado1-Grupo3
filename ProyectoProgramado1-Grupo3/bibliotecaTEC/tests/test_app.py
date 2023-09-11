# Pruebas unitarias
import unittest
from bibliotecaTEC.src.app import * # Asegúrate de importar la app y mongo desde tu aplicación
from bibliotecaTEC.src.models import * # Asegúrate de importar los modelos necesarios

class TestApp(unittest.TestCase):

    def setUp(self):
        # Configurar la aplicación para el entorno de pruebas
        app.config['TESTING'] = True
        self.app = app.test_client()
        self.mongo = mongo

    def tearDown(self):
        # Limpiar la base de datos después de cada prueba
        self.mongo.db.drop_collection('usuarios')
        self.mongo.db.drop_collection('libros')
        self.mongo.db.drop_collection('alquileres')

    def test_registro_de_usuario(self):
        # Prueba de registro de un nuevo usuario
        response = self.app.post('/registrar_usuario', json={'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 200)

    def test_inicio_de_sesion(self):
        # Prueba de inicio de sesión con credenciales válidas
        self.app.post('/registrar_usuario', json={'username': 'testuser', 'password': 'testpassword'})
        response = self.app.post('/login', json={'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 200)

    def test_alquiler_de_libro(self):
        # Prueba de alquiler de un libro por un usuario autenticado
        user = User(username='testuser')
        book = Book(title='Test Book', available=True)
        self.mongo.db.usuarios.insert_one(user.to_dict())
        self.mongo.db.libros.insert_one(book.to_dict())
        
        # Iniciar sesión como el usuario
        self.app.post('/login', json={'username': 'testuser', 'password': 'testpassword'})

        # Alquilar el libro
        response = self.app.post('/rent_book', json={'book_id': str(book.id)})
        self.assertEqual(response.status_code, 200)

    # Agrega más pruebas según sea necesario

if __name__ == '__main__':
    unittest.main()

# Correr con python test_app.py