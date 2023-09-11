# Código principal de la aplicación

import json
from bibliotecaTEC.src.models import Alquiler, Book, User, Rental
from flask import Flask, request, jsonify, g
from flask_pymongo import PyMongo
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient
from datetime import datetime, timedelta

# Configura la conexión al clúster de MongoDB
mongo_client = MongoClient("mongodb://192.168.100.137:27018,192.168.100.138:27018,192.168.100.139:27018/?replicaSet=my-replica-set")
app = Flask(__name__)
# Accede a una base de datos específica en el clúster
db = mongo_client.bibliotecaTEC
app.router['MONGO_URI'] = 'mongodb://192.168.100.137:27018/bibliotecaTEC'
app.shard['MONGO_URI'] = 'mongodb://192.168.100.138:27018/bibliotecaTEC'
app.config['MONGO_URI'] = 'mongodb://192.168.100.139:27018/bibliotecaTEC'

app.secret_key = 'your_secret_key'
mongo = PyMongo(app)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

# Clase para representar un usuario
class Usuario(UserMixin):
    def __init__(self, username):
        self.username = username

# Clase para representar un config
class Config:
    def __init__(self, nombre, ip, puerto):
        self.nombre = nombre
        self.ip = ip
        self.puerto = puerto
        self.tipo = 'config'

# Clase para representar un router
class Router:
    def __init__(self, nombre, ip, puerto):
        self.nombre = nombre
        self.ip = ip
        self.puerto = puerto
        self.tipo = 'router'

# Clase para representar un shard
class Shard:
    def __init__(self, nombre, ip, puerto):
        self.nombre = nombre
        self.ip = ip
        self.puerto = puerto
        self.tipo = 'shard'


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

# Información de los servidores de configuración
config = {
    'Sirio': Config('Cartago', 'Oriental', 'localhost', 27019),
    'Aldebaran': Config('SanJose', 'SanJose', 'localhost', 27019),
    'Elnath': Config('SanJose', 'MontesDeOca', 'localhost', 27019)
}

# Información de los routers
routers = {
    'Antares': Router('Cartago', 'Orienta', 'localhost', 27017),
    'Shaula': Router('SanJose', 'SanJose', 'localhost', 27017),
    'Sargas': Router('SanJose', 'MontesdeOca', 'localhost', 27017)
}

# Información de los shards
shards = {
    'Betelgeuse': Shard('SanCarlos', 'SantaClara', 'localhost', 27018),
    'Rigel': Shard('Limon', 'SanJose', 'localhost', 27018),
    'Alnilam': Shard('Alajuela', 'MontesDeOca', 'localhost', 27018)
}

# Conexión a MongoDB en cada nodo
def conectar_a_mongodb(nodo):
    client = MongoClient(nodo.ip, nodo.puerto)
    db = client.bibliotecaTEC  # Nombre de la base de datos
    return db

# Registro de usuarios y alquileres
usuarios = []
libros = []
alquileres = []

# Conexión de nodos con servidores de configuración
nodos_config = {
    'Cartago': 'config-CanMayor',
    'SanJose': 'config-CanMayor',
    'SanJoseMontesDeOca': 'config-CanMayor'
}

# Conexión de nodos con servidores de router
nodos_router = {
    'CartagoOriental': 'router-scorpio',
    'SanJoseSanJose': 'router-scorpio',
    'SanJoseMontesDeOca': 'router-scorpio'
}

# Conexión de nodos con servidores de shard
nodos_shard = {
    'SanCarlosSantaClara': 'shard-orion',
    'LimonSanJose': 'shard-orion',
    'AlajuelaMontesDeOca': 'shard-orion'
}

# Cargar la base de datos de libros desde bsamazon.json
with open('bsamazon.json', 'r') as file:
    libros = json.load(file)

# Definir modelo de usuario
class User(UserMixin):
    def __init__(self, username):
        self.username = username

# Implementar funciones de carga de usuario
@login_manager.user_loader
def load_user(username):
    return User(username)

# Endpoint para iniciar sesión
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = mongo.db.usuarios.find_one({'username': username})

    if user and check_password_hash(user['password'], password):
        user_obj = User(username)
        login_user(user_obj)
        return jsonify({'mensaje': 'Inicio de sesión exitoso'})

    return jsonify({'error': 'Credenciales incorrectas'}), 401

# Endpoint para cerrar sesión
@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'mensaje': 'Sesión cerrada'})

# Middleware para verificar si el usuario está autenticado
@app.before_request
def before_request():
    g.user = current_user

# Endpoint para obtener información de cualquier nodo
def obtener_info_nodo(nombre):
    libros_disponibles = obtener_libros_disponibles
    if nombre in nodos_config:
        return jsonify({'info': f'Información del config {obtener_info_config(nombre)}' + libros_disponibles}) 
    elif nombre in nodos_router:
        return jsonify({'info': f'Información del router {obtener_info_router(nombre)}' + libros_disponibles})
    elif nombre in nodos_shard:
        return jsonify({'info': f'Información del shard {obtener_info_shard(nombre)}' + libros_disponibles})
    else:
        return jsonify({'error': 'Nodo no encontrado'}), 404

# Función para obtener información del servidor de configuración
def obtener_info_config(nodo):
    if nodo.nombre in nodos_config:
        configuracion = nodos_config[nodo.nombre]
        return {'info': f'Servidor de router en {configuracion.ip}:{configuracion.puerto}', 'tipo': 'config'}
    else:
        return {'info': 'No hay servidor de router asignado para este nodo'}
    
# Función para obtener información del servidor de router
def obtener_info_router(nodo):
    if nodo.nombre in nodos_router:
        router = nodos_router[nodo.nombre]
        return {'info': f'Servidor de router en {router.ip}:{router.puerto}', 'tipo': 'router'}
    else:
        return {'info': 'No hay servidor de router asignado para este nodo'}

# Función para obtener información del servidor de shard
def obtener_info_shard(nodo):
    if nodo.nombre in nodos_shard:
        shard = nodos_shard[nodo.nombre]
        return {'info': f'Servidor de shard en {shard.ip}:{shard.puerto}', 'tipo': 'shard'}
    else:
        return {'info': 'No hay servidor de shard asignado para este nodo'}

# Función para obtener información del nodo desde MongoDB
def obtener_info_nodo_mongodb(db):
    try:
        # Puedes realizar consultas a la base de datos MongoDB aquí y obtener información específica
        # de la sede/nodo. Por ejemplo, puedes consultar información de libros en la sede.
        # Supongamos que tienes una colección llamada "informacion_sede" en MongoDB.
        informacion_sede = db.informacion_sede.find_one()
        if informacion_sede:
            return informacion_sede
        else:
            return {'info': 'Información del nodo desde MongoDB no encontrada'}
    except Exception as e:
        return {'error': f'Error al obtener información del nodo desde MongoDB: {str(e)}'}

#Función para obtener la lista de libros disponibles en un nodo
def obtener_libros_disponibles(nodo):
    try:
        db = conectar_a_mongodb(nodo)
        libros_disponibles = obtener_libros_disponibles_mongodb(db)
        return libros_disponibles
    except Exception as e:
        return {'error': f'Error al obtener libros disponibles en el nodo {nodo.nombre}: {str(e)}'}

# Función para obtener libros disponibles en MongoDB
def obtener_libros_disponibles_mongodb(db):
    try:
        # Puedes realizar consultas a la base de datos MongoDB aquí para obtener la lista de libros disponibles.
        # Supongamos que tienes una colección llamada "libros" en MongoDB y cada documento representa un libro.
        libros_disponibles = list(db.libros.find({'disponible': True}))
        if libros_disponibles:
            return libros_disponibles
        else:
            return {'info': 'No hay libros disponibles en MongoDB'}
    except Exception as e:
        return {'error': f'Error al obtener libros disponibles desde MongoDB: {str(e)}'}

# Endpoint para obtener la lista de libros disponibles en un nodo
@app.route('/libros_disponibles/<nombre>', methods=['GET'])
def obtener_libros_disponibles_nodo(nombre):
    if nombre in nodos:
        nodo = nodos[nombre]
        libros_disponibles = obtener_libros_disponibles(nodo)
        return jsonify({'libros_disponibles': libros_disponibles})
    else:
        return jsonify({'error': 'Nodo no encontrado'}), 404

# Endpoint para realizar asignación de recursos
@app.route('/asignar_recursos/<nombre>', methods=['POST'])
def asignar_recursos(nombre):
    if nombre in nodos_config:
        return asignar_recursos_config(nombre)
    elif nombre in nodos_router:
        return asignar_recursos_router(nombre)
    elif nombre in nodos_shard:
        return asignar_recursos_shard(nombre)
    else:
        return jsonify({'error': 'Nodo no encontrado'}), 404

# Función para asignar recursos al servidor de configuración
def asignar_recursos_config(nodos_config, recursos):
    try:
        config_db = conectar_a_mongodb(config[nodos_config])
        recursos_collection = config_db['recursos']
        recursos_collection.insert_one({'recursos': recursos})
    except Exception as e:
        return jsonify({'error': f'Error al asignar recursos al servidor de configuración: {str(e)}'}), 500

# Función para asignar recursos al servidor de routers
def asignar_recursos_router(nodos_router, recursos):
    try:
        routers_db = conectar_a_mongodb(routers[nodos_router])
        recursos_collection = routers_db['recursos']
        recursos_collection.insert_one({'recursos': recursos})
    except Exception as e:
        return jsonify({'error': f'Error al asignar recursos al servidor de configuración: {str(e)}'}), 500
    
# Función para asignar recursos al servidor de shards
def asignar_recursos_shard(nodos_shard, recursos):
    try:
        shards_db = conectar_a_mongodb(shards[nodos_shard])
        recursos_collection = shards_db['recursos']
        recursos_collection.insert_one({'recursos': recursos})
    except Exception as e:
        return jsonify({'error': f'Error al asignar recursos al servidor de configuración: {str(e)}'}), 500

# Endpoint para realizar fragmentación de la base de datos
@app.route('/fragmentar', methods=['POST'])
def fragmentar():
    data = request.json
    criterio = data.get('criterio')

    # Lógica para fragmentar la base de datos según el criterio
    if criterio == 'genero':
        fragmentar_por_genero()
        return jsonify({'mensaje': 'Base de datos fragmentada por género'})
    elif criterio == 'ubicacion':
        fragmentar_por_ubicacion()
        return jsonify({'mensaje': 'Base de datos fragmentada por ubicación'})
    else:
        return jsonify({'error': 'Criterio de fragmentación no válido'}), 400


# Función para fragmentar la base de datos por género literario
def fragmentar_por_genero():
    # Lógica para fragmentar la base de datos por género literario
    for genero in set(libro.genre for libro in Book.query.all()):
        # Crear una colección para cada género literario
        libros_genero = Book.query.filter_by(genre=genero).all()
        for libro in libros_genero:
            libro_collection = db.get_collection(genero)
            libro_collection.insert_one(libro.to_dict())  # Agregar libros a la colección

        # Eliminar los libros originales de la colección principal
        Book.query.filter_by(genre=genero).delete()
        db.session.commit()


# Función para fragmentar la base de datos por ubicación geográfica
def fragmentar_por_ubicacion():
    # Lógica para fragmentar la base de datos por ubicación geográfica
    for libro in libros:
        if libro['location'] in nodos:
            nodo = nodos[libro['location']]
            try:
                db = conectar_a_mongodb(nodo)
                if libro['location'] not in db.list_collection_names():
                    db.create_collection(libro['location'])
                db[libro['location']].insert_one(libro)
            except Exception as e:
                print(f'Error al fragmentar la base de datos en el nodo {nodo.nombre}: {str(e)}')

# Endpoint para registrar un usuario
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

# Endpoint para alquilar un libro
@app.route('/alquilar_libro', methods=['POST'])
@login_required
def alquilar_libro():
    data = request.json
    libro_id = data.get('libro_id')
    ubicacion_usuario = data.get('ubicacion_usuario')
    campus_usuario = data.get('campus_usuario')

    # Verificar si el libro está disponible
    libro = Book.query.get(libro_id)
    if libro:
        if libro.available:
            usuario_id = current_user.id
            fecha_alquiler = datetime.now()
            fecha_devolucion = fecha_alquiler + timedelta(days=15)
            fecha_vencimiento = fecha_alquiler + timedelta(days=30)  # Considerar 30 días como fecha de vencimiento
            nuevo_alquiler = Alquiler(usuario_id=usuario_id, libro_id=libro_id,
                                       fecha_alquiler=fecha_alquiler,
                                       fecha_devolucion=fecha_devolucion,
                                       estado_devolucion=False,
                                       multa=0,
                                       ubicacion_usuario=ubicacion_usuario,
                                       campus_usuario=campus_usuario,
                                       fecha_vencimiento=fecha_vencimiento)
            db.session.add(nuevo_alquiler)
            libro.available = False
            db.session.commit()
            return jsonify({'mensaje': 'Libro alquilado correctamente'})
        else:
            return jsonify({'error': 'Libro no disponible para alquilar'}), 400
    else:
        return jsonify({'error': 'Libro no encontrado'}), 404

# Endpoint para devolver un libro
@app.route('/devolver_libro', methods=['POST'])
@login_required
def devolver_libro():
    data = request.json
    libro_id = data.get('libro_id')

    # Buscar el alquiler correspondiente
    alquiler = Alquiler.query.filter_by(libro_id=libro_id, usuario_id=current_user.id,
                                        estado_devolucion=False).first()
    if alquiler:
        libro = Book.query.get(libro_id)
        fecha_devolucion = datetime.now()
        dias_retraso = (fecha_devolucion - alquiler.fecha_vencimiento).days
        calificacion = libro.user_rating
        multa = calcular_multa(dias_retraso, calificacion)

        # Actualizar el estado de devolución y la multa en el registro de alquiler
        alquiler.estado_devolucion = True
        alquiler.multa = multa

        # Marcar el libro como disponible nuevamente
        libro.available = True
        db.session.commit()

        return jsonify({'mensaje': 'Libro devuelto correctamente'})
    else:
        return jsonify({'error': 'Libro no encontrado o no pertenece al usuario o ya ha sido devuelto'}), 404

# Función para calcular multas por retraso
def calcular_multa(dias_retraso, calificacion):
    multa_base = 2000
    if calificacion >= 4:
        multa_base = 3500
    return dias_retraso * multa_base


# Endpoint para marcar un libro como extraviado
@app.route('/marcar_extraviado', methods=['POST'])
def marcar_extraviado():
    data = request.json
    libro_id = data.get('libro_id')
    ubicacion = data.get('ubicacion')  # Agrega la ubicación del libro en el JSON

    # Lógica para marcar un libro como extraviado en la base de datos MongoDB
    try:
        if ubicacion in nodos_shard:
            # Si la ubicación está en un shard, realiza la operación en ese shard
            shard = nodos_shard[ubicacion]
            db = conectar_a_mongodb(shard)
            libro = db.libros.find_one({'_id': libro_id})

            if libro:
                # Actualiza el estado del libro a extraviado
                db.libros.update_one({'_id': libro_id}, {'$set': {'extraviado': True}})
                return jsonify({'mensaje': 'Libro marcado como extraviado correctamente'})
            else:
                return jsonify({'error': 'Libro no encontrado en el shard'}), 404
        else:
            return jsonify({'error': 'Ubicación no válida'}), 400
    except Exception as e:
        return jsonify({'error': f'Error al marcar el libro como extraviado: {str(e)}'}), 500



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
