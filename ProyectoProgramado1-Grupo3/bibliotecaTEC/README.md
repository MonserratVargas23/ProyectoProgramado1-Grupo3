Proyecto Programado 1 - Diseño e implementación de una base de datos distribuida
Celeste Monge, Janys Torres y Monserrat Vargas
Bases de Datos Avanzadas. Grupo 03

Ubicacion del los nueve nodos correspondientes al cluster:
https://drive.google.com/drive/folders/1PWMMwqlLmXQ6T65iLcKJHWJJ18EcAa1U

El proyecto consta de tres archivos principales: `app.py`, `models.py` y `routes.py`. A continuación, se proporciona un resumen del contenido de cada archivo para el archivo `README.md`:

### Archivo `app.py`

Este archivo contiene la lógica principal de la aplicación web Flask. Algunos puntos clave son:

- Configuración de la conexión a MongoDB en varios nodos.
- Definición de las rutas y endpoints de la aplicación, incluyendo el inicio de sesión, cierre de sesión, y la gestión de alquileres de libros.
- Implementación de funciones para el inicio de sesión y el registro de usuarios.
- Manejo de la fragmentación de la base de datos por género literario o ubicación geográfica.
- Uso de Flask-Login para gestionar la autenticación de usuarios.

### Archivo `models.py`

Este archivo define los modelos de datos utilizando SQLAlchemy. Algunos puntos clave son:

- Definición de las clases `Book`, `User`, `Alquiler` para representar libros, usuarios y alquileres de libros.
- Configuración de relaciones entre las clases para gestionar los alquileres de libros por usuarios.
- Creación de una base de datos SQLite para almacenar los datos de la aplicación.

### Archivo `routes.py`

Este archivo define las rutas y controladores de la aplicación web. Algunos puntos clave son:

- Implementación de rutas para obtener información de nodos, alquilar libros y realizar otras acciones relacionadas con la aplicación.
- Uso de Flask-Login para gestionar la autenticación de usuarios y proteger rutas específicas.
- Consultas a la base de datos para obtener información sobre libros y alquileres de libros.
- Manejo de la conexión a MongoDB para obtener información de nodos y gestionar libros extraviados.

Este resumen debería proporcionar una visión general de la estructura y funcionalidad de la aplicación. Asegúrate de proporcionar instrucciones adicionales, requisitos o configuraciones específicas en el archivo `README.md` para que los usuarios puedan entender y ejecutar la aplicación correctamente.
