import sqlite3
from constantes import NOMBRE_BASE_DE_DATOS

def crear_tablas_db():
    """
    Crea las tablas necesarias en la base de datos.

    Parámetros:
        Ninguno.
    
    Retorna:
        Nada.
    """
    try:
        conexion = sqlite3.connect(NOMBRE_BASE_DE_DATOS)
        conexion.execute('''CREATE TABLE IF NOT EXISTS jugadores (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT,
                        puntuacion INTEGER
                    )''')
        conexion.close()
    except sqlite3.OperationalError:
        print("La tabla personajes ya existe")

def insertar_jugador(nombre, puntuacion):
    """
    Inserta un nuevo jugador en la base de datos.

    Parámetros:
        nombre: nombre del jugador.
        puntuacion: puntuación del jugador.
    
    Retorna:
        Nada.
    """
    try:
        conexion = sqlite3.connect(NOMBRE_BASE_DE_DATOS)
        conexion.execute("INSERT INTO jugadores (nombre, puntuacion) VALUES (?, ?)", (nombre, puntuacion))
        conexion.commit()
        conexion.close()
    except:
        print("Error")

def obtener_ranking():
    """
    Obtiene el ranking desde la base de datos.

    Parámetros:
        Ninguno.
    
    Retorna:
        ranking: Una lista que contienen el nombre y la puntuación de los jugadores.
    """
    try:
        conexion = sqlite3.connect(NOMBRE_BASE_DE_DATOS)
        cursor = conexion.execute("SELECT nombre, puntuacion FROM jugadores ORDER BY puntuacion DESC")
        ranking = cursor.fetchall()
        conexion.close()
        return ranking
    except:
        print("Error")
