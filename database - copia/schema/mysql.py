"""
Archivo de prueba para verificar conexión a MySQL
Usa la clase centralizada DatabaseConnection desde db_connection.py
"""

import os
from dotenv import load_dotenv
from database.db_connection import DatabaseConnection

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Crear conexión usando la clase centralizada
db = DatabaseConnection()

if db.connect():
    print(f"Conectado a la base de datos MySQL en {db.host} como {db.user}")
    cursor = db.cursor()
    cursor.execute("SELECT VERSION()")
    db_version = cursor.fetchone()
    print(f"Versión de MySQL: {db_version[0]}")
    cursor.close()
    db.disconnect()
else:
    print("No se pudo establecer la conexión a la base de datos")