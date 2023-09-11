# Definición de modelos de datos

from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from pymongo import MongoClient

Base = declarative_base()

# Conexión a MongoDB en cada nodo
def conectar_a_mongodb(nodo):
    client = MongoClient(nodo.ip, nodo.puerto)
    db = client.bibliotecaTEC  # Nombre de la base de datos
    return db

class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    user_rating = Column(Float)
    reviews = Column(Integer)
    price = Column(Float)
    year = Column(Integer)
    genre = Column(String)
    available = Column(Boolean, default=True)

    alquileres = relationship("Alquiler", back_populates="libro")

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    roles = Column(String)  # Puedes agregar roles para la gestión de permisos

    alquileres = relationship("Alquiler", back_populates="usuario")

class Rental(Base):
    __tablename__ = 'rentals'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    book_id = Column(Integer, ForeignKey('books.id'))
    rental_date = Column(Date)

    # Definir relaciones
    user = relationship("User", back_populates="rentals")
    book = relationship("Book", back_populates="rentals")

# Definir un modelo para representar libros alquilados por usuarios
class Alquiler(Base):
    __tablename__ = 'alquileres'

    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey('users.id'))
    libro_id = Column(Integer, ForeignKey('books.id'))
    fecha_alquiler = Column(Date)
    fecha_devolucion = Column(Date)
    estado_devolucion = Column(Boolean)
    multa = Column(Integer)
    ubicacion_usuario = Column(String)  # Ubicación del usuario
    campus_usuario = Column(String)  # Campus donde se encuentra matriculado el usuario
    fecha_vencimiento = Column(Date)  # Fecha de vencimiento del libro

    usuario = relationship("User", back_populates="alquileres")
    libro = relationship("Book", back_populates="alquileres")

# Agregar relaciones inversas a las clases User y Book
User.alquileres = relationship("Alquiler", order_by=Alquiler.id, back_populates="usuario")
Book.alquileres = relationship("Alquiler", order_by=Alquiler.id, back_populates="libro")
