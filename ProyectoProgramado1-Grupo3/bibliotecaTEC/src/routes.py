import json
from bibliotecaTEC.src.app import *
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.router['MONGO_URI'] = 'mongodb://192.168.100.137:27018/bibliotecaTEC'
app.shard['MONGO_URI'] = 'mongodb://192.168.100.138:27018/bibliotecaTEC'
app.config['MONGO_URI'] = 'mongodb://192.168.100.139:27018/bibliotecaTEC'
mongo = PyMongo(app)
app.secret_key = 'your_secret_key'

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

# Información de los nodos
nodos = {
    'sirio': Config('sirio', '192.168.100.137', 27018),
    'aldebaran': Config('aldebaran', '192.168.100.138', 27018),
    'elnath': Config('elnath', '192.168.100.139', 27018),
    'betelgeuse': Shard('betelgeuse', '192.168.100.140', 27018),
    'rigel': Shard('rigel', '192.168.100.141', 27018),
    'alnilam': Shard('alnilam', '192.168.100.142', 27018),
    'antares': Router('antares', '192.168.100.143', 27017),
    'shaula': Router('shaula', '192.168.100.144', 27017),
    'sargas': Router('sargas', '192.168.100.145', 27017),
}

# Clase para representar un usuario
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    roles = db.Column(db.String(120)) 

    alquileres = db.relationship("Alquiler", back_populates="usuario")

# Clase para representar un libro
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    author = db.Column(db.String(255))
    user_rating = db.Column(db.Float)
    reviews = db.Column(db.Integer)
    price = db.Column(db.Float)
    year = db.Column(db.Integer)
    genre = db.Column(db.String(255))
    available = db.Column(db.Boolean, default=True)

    alquileres = db.relationship("Alquiler", back_populates="libro")

# Clase para representar un alquiler
class Alquiler(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    libro_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    fecha_alquiler = db.Column(db.Date)
    fecha_devolucion = db.Column(db.Date)
    estado_devolucion = db.Column(db.Boolean)
    multa = db.Column(db.Integer)
    ubicacion_usuario = db.Column(db.String(255))  # Ubicación del usuario
    campus_usuario = db.Column(db.String(255))  # Campus donde se encuentra matriculado el usuario
    fecha_vencimiento = db.Column(db.Date)  # Fecha de vencimiento del libro

    usuario = db.relationship("User", back_populates="alquileres")
    libro = db.relationship("Book", back_populates="alquileres")

# Implementar funciones de carga de usuario
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Endpoint para iniciar sesión
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        user_obj = User(username)
        login_user(user_obj)
        return jsonify({'mensaje': 'Inicio de sesión exitoso'})

    return jsonify({'error': 'Credenciales incorrectas'}), 401

@app.route('/registrar_usuario', methods=['POST'])
def registrar_usuario():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Verificar si el usuario ya existe
    if mongo.db.usuarios.find_one({'username': username}):
        return jsonify({'error': 'El usuario ya existe'}), 400

    # Crear un nuevo usuario en la base de datos
    hashed_password = generate_password_hash(password, method='sha256')
    mongo.db.usuarios.insert_one({'username': username, 'password': hashed_password})
    return jsonify({'mensaje': 'Usuario registrado correctamente'})


# Endpoint para cerrar sesión
@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'mensaje': 'Sesión cerrada'})

# Ruta del panel de control (dashboard)
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

# Rutas y controladores
@app.route('/books', methods=['GET'])
def get_books():
    # Implementa la lógica para consultar libros y enviar una respuesta JSON
    books = Book.query.all()
    book_list = [{'id': book.id, 'title': book.title, 'author': book.author} for book in books]
    return jsonify({'books': book_list})

@app.route('/rentals', methods=['POST'])
@login_required
def rent_book():
    # Implementa la lógica para alquilar un libro
    data = request.json
    book_id = data.get('book_id')

    book = Book.query.get(book_id)

    if book and book.available:
        # Realiza el alquiler
        alquiler = Alquiler(usuario_id=current_user.id, libro_id=book_id)
        db.session.add(alquiler)
        book.available = False
        db.session.commit()
        return jsonify({'mensaje': 'Libro alquilado correctamente'})
    else:
        return jsonify({'error': 'Libro no disponible para alquilar'}), 400

@app.route('/nodo/<nombre>', methods=['GET'])
def obtener_info_nodo(nombre):
    if nombre in nodos:
        nodo = nodos[nombre]
        try:
            db = conectar_a_mongodb(nodo)
            config_info = obtener_info_config(nodo)
            nodo_info = obtener_info_nodo_mongodb(db)
            libros_disponibles = obtener_libros_disponibles(nodo)
            return jsonify({'nodo_info': nodo_info, 'config_info': config_info, 'libros_disponibles': libros_disponibles})
        except Exception as e:
            return jsonify({'error': f'Error al conectarse al nodo {nombre}: {str(e)}'}), 500
    elif nombre in nodos_router:
        router = nodos_router[nombre]
        router_info = obtener_info_router(router)
        return jsonify({'router_info': router_info})
    elif nombre in nodos_shard:
        shard = nodos_shard[nombre]
        shard_info = obtener_info_shard(shard)
        return jsonify({'shard_info': shard_info})
    else:
        return jsonify({'error': 'Nodo no encontrado'}), 404


class Usuario(UserMixin):
    def __init__(self, username):
        self.username = username
        self.alquileres = []

@app.route('/alquileres', methods=['GET'])
@login_required
def obtener_alquileres_usuario():
    # Obtener alquileres del usuario autenticado
    usuario = Usuario(g.user.username)
    alquileres_usuario = usuario.alquileres
    return jsonify({'alquileres': alquileres_usuario})


if __name__ == '__main__':
    db.create_all()  # Crear las tablas en la base de datos si no existen
    app.run(host='0.0.0.0', port=5000)
