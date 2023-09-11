import tkinter as tk
import json
import requests



def enviar_datos_a_antares(libro):
    
    url_antares = "http://192.168.100.143:8080/~/antares-cse/antares-id/your_table"  
    
    headers = {
        "X-M2M-Origin": "your_app_id",  
        "Content-Type": "application/json;ty=4",
        "X-M2M-RI": "12345"
    }
    
   
    data = {
        "m2m:cin": {
            "con": json.dumps(libro)
        }
    }
    
    
    response = requests.post(url_antares, headers=headers, json=data)
    
    
    if response.status_code == 201:
        print("Datos enviados a Antares exitosamente.")
    else:
        print("Error al enviar datos a Antares:", response.status_code)

# Base de datos de libros
base_de_datos = []

# Función para crear un nuevo registro de libro
def crear_registro():
    titulo = entrada_titulo.get()
    autor = entrada_autor.get()
    rating = entrada_rating.get()
    reviews = entrada_reviews.get()
    precio = entrada_precio.get()
    anio = entrada_anio.get()
    genero = entrada_genero.get()
    
    if titulo and autor and rating and reviews and precio and anio and genero:
        libro = {
            "Título": titulo,
            "Autor": autor,
            "User Rating": rating,
            "Reviews": reviews,
            "Precio": precio,
            "Año": anio,
            "Género": genero
        }
        base_de_datos.append(libro)
        resultado_consulta.insert(tk.END, "Libro creado:\n")
        resultado_consulta.insert(tk.END, f"Título: {titulo}\n")
        resultado_consulta.insert(tk.END, f"Autor: {autor}\n")
        resultado_consulta.insert(tk.END, f"User Rating: {rating}\n")
        resultado_consulta.insert(tk.END, f"Reviews: {reviews}\n")
        resultado_consulta.insert(tk.END, f"Precio: ${precio}\n")
        resultado_consulta.insert(tk.END, f"Año: {anio}\n")
        resultado_consulta.insert(tk.END, f"Género: {genero}\n")
        resultado_consulta.insert(tk.END, "\n")
    else:
        resultado_consulta.insert(tk.END, "Por favor, complete todos los campos.\n")

# Función para leer todos los registros de libros
def leer_registros():
    resultado_consulta.delete(1.0, tk.END)
    if base_de_datos:
        resultado_consulta.insert(tk.END, "Lista de Libros:\n")
        for libro in base_de_datos:
            resultado_consulta.insert(tk.END, f"Título: {libro['Título']}\n")
            resultado_consulta.insert(tk.END, f"Autor: {libro['Autor']}\n")
            resultado_consulta.insert(tk.END, f"User Rating: {libro['User Rating']}\n")
            resultado_consulta.insert(tk.END, f"Reviews: {libro['Reviews']}\n")
            resultado_consulta.insert(tk.END, f"Precio: ${libro['Precio']}\n")
            resultado_consulta.insert(tk.END, f"Año: {libro['Año']}\n")
            resultado_consulta.insert(tk.END, f"Género: {libro['Género']}\n")
            resultado_consulta.insert(tk.END, "\n")
    else:
        resultado_consulta.insert(tk.END, "No hay libros en la base de datos.\n")

# Función para borrar todos los registros de libros
def borrar_registros():
    base_de_datos.clear()
    resultado_consulta.delete(1.0, tk.END)
    resultado_consulta.insert(tk.END, "Todos los libros han sido borrados.\n")

# Función para consultar información de libros
def consultar_libros():
    resultado_consulta.delete(1.0, tk.END)
    if base_de_datos:
        resultado_consulta.insert(tk.END, "Lista de Libros:\n")
        for libro in base_de_datos:
            resultado_consulta.insert(tk.END, f"Título: {libro['Título']}\n")
            resultado_consulta.insert(tk.END, f"Autor: {libro['Autor']}\n")
            resultado_consulta.insert(tk.END, f"User Rating: {libro['User Rating']}\n")
            resultado_consulta.insert(tk.END, f"Reviews: {libro['Reviews']}\n")
            resultado_consulta.insert(tk.END, f"Precio: ${libro['Precio']}\n")
            resultado_consulta.insert(tk.END, f"Año: {libro['Año']}\n")
            resultado_consulta.insert(tk.END, f"Género: {libro['Género']}\n")
            resultado_consulta.insert(tk.END, "\n")
    else:
        resultado_consulta.insert(tk.END, "No hay libros en la base de datos.\n")

# Función para consultar información de préstamos de libros
def consultar_prestamos():
    # Aquí puedes implementar la lógica para consultar préstamos de libros
    # Puedes mostrar la información de los préstamos en el área de resultado_consulta
    resultado_consulta.delete(1.0, tk.END)
    resultado_consulta.insert(tk.END, "Información de Préstamos de Libros:\n")
    # Agrega lógica para consultar y mostrar información de préstamos aquí

# Crear una ventana
ventana_principal = tk.Tk()
ventana_principal.geometry("800x600")
ventana_principal.title("Biblioteca")
ventana_principal.configure(bg="aquamarine3")

# Crear marcos para organizar la interfaz
marco_superior = tk.Frame(ventana_principal)
marco_superior.pack(pady=20)

marco_medio = tk.Frame(ventana_principal)
marco_medio.pack(pady=20)

marco_inferior = tk.Frame(ventana_principal)
marco_inferior.pack(pady=20)

# Etiquetas y entradas para crear registros
etiqueta_titulo = tk.Label(marco_superior, text="Título:")
etiqueta_titulo.pack()

entrada_titulo = tk.Entry(marco_superior, width=50)
entrada_titulo.pack()

etiqueta_autor = tk.Label(marco_superior, text="Autor:")
etiqueta_autor.pack()

entrada_autor = tk.Entry(marco_superior, width=50)
entrada_autor.pack()

etiqueta_rating = tk.Label(marco_superior, text="User Rating:")
etiqueta_rating.pack()

entrada_rating = tk.Entry(marco_superior, width=50)
entrada_rating.pack()

etiqueta_reviews = tk.Label(marco_superior, text="Reviews:")
etiqueta_reviews.pack()

entrada_reviews = tk.Entry(marco_superior, width=50)
entrada_reviews.pack()

etiqueta_precio = tk.Label(marco_superior, text="Precio ($):")
etiqueta_precio.pack()

entrada_precio = tk.Entry(marco_superior, width=50)
entrada_precio.pack()

etiqueta_anio = tk.Label(marco_superior, text="Año:")
etiqueta_anio.pack()

entrada_anio = tk.Entry(marco_superior, width=50)
entrada_anio.pack()

etiqueta_genero = tk.Label(marco_superior, text="Género:")
etiqueta_genero.pack()

entrada_genero = tk.Entry(marco_superior, width=50)
entrada_genero.pack()

# Botones para operaciones CRUD
btn_crear = tk.Button(marco_superior, text="Crear Registro", command=crear_registro)
btn_crear.pack(side=tk.LEFT, padx=10)

btn_leer = tk.Button(marco_superior, text="Leer Registros", command=leer_registros)
btn_leer.pack(side=tk.LEFT, padx=10)

btn_borrar = tk.Button(marco_superior, text="Borrar Registros", command=borrar_registros)
btn_borrar.pack(side=tk.LEFT, padx=10)

# Botones para operaciones de consulta para bibliotecarios de nivel 1
btn_consultar_libros = tk.Button(marco_superior, text="Consultar Libros", command=consultar_libros)
btn_consultar_libros.pack(side=tk.LEFT, padx=10)

btn_consultar_prestamos = tk.Button(marco_superior, text="Consultar Préstamos", command=consultar_prestamos)
btn_consultar_prestamos.pack(side=tk.LEFT, padx=10)

# Área para mostrar resultados de la consulta
resultado_consulta = tk.Text(marco_inferior, width=70, height=15)
resultado_consulta.pack()

# Ejecutar la ventana principal
ventana_principal.mainloop()