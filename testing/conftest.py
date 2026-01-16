"""
conftest.py - Configuración compartida para todos los tests
Contiene: DatabaseManager + pytest fixture
"""

import pytest
import mysql.connector
from mysql.connector import Error
import os
from pathlib import Path

# Cargar variables de entorno desde .env (si existe)
try:
    from dotenv import load_dotenv
    # Buscar .env en la carpeta padre (raiz del proyecto)
    env_path = Path(__file__).parent.parent / '.env'
    load_dotenv(dotenv_path=env_path)
except ImportError:
    pass  # Si python-dotenv no está instalado, usa valores por defecto

# Valores por defecto (se pueden sobrescribir con variables de entorno)
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'inacap_test')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_NAME = os.getenv('DB_NAME', 'inacap_test')
DB_PORT = int(os.getenv('DB_PORT', '3306'))


class DatabaseManager:
    """Clase para manejar la conexión a la base de datos"""
    
    def __init__(self, host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None
    
    def connect(self):
        """Conectar a la base de datos"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            self.cursor = self.connection.cursor()
            print(f"\n✓ Conectado a la base de datos: {self.database}")
            return True
        except Error as e:
            print(f"\n✗ Error al conectar: {e}")
            return False
    
    def disconnect(self):
        """Desconectar de la base de datos"""
        if self.connection and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("✓ Desconectado de la base de datos")
    
    def execute_query(self, query, values=None):
        """Ejecutar una query de inserción/actualización"""
        try:
            if values:
                self.cursor.execute(query, values)
            else:
                self.cursor.execute(query)
            self.connection.commit()
            return True, None
        except Error as e:
            self.connection.rollback()
            return False, str(e)
    
    def fetch_query(self, query, values=None):
        """Ejecutar una query SELECT"""
        try:
            if values:
                self.cursor.execute(query, values)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchall()
        except Error as e:
            return None
    
    def clear_tables(self):
        """Limpiar todas las tablas (respetando foreign keys)"""
        try:
            # Deshabilitar constraint checks temporalmente
            self.cursor.execute("SET FOREIGN_KEY_CHECKS=0")
            
            tables = [
                'PredictorDatos',
                'HistorialInstitucional',
                'estudiante_direccion',
                'estudiante_colegio',
                'Direccion',
                'Estudiante',
                'Colegio',
                'Comuna',
                'Region'
            ]
            
            for table in tables:
                try:
                    self.cursor.execute(f"TRUNCATE TABLE {table}")
                except Error:
                    pass
            
            # Reabilitar constraint checks
            self.cursor.execute("SET FOREIGN_KEY_CHECKS=1")
            self.connection.commit()
            print("✓ Tablas vaciadas exitosamente")
            return True
        except Error as e:
            self.connection.rollback()
            print(f"✗ Error al limpiar tablas: {e}")
            return False


# ===== PYTEST FIXTURE =====

@pytest.fixture(scope="function")
def db():
    """Fixture para inicializar y cerrar la conexión a BD"""
    db_manager = DatabaseManager()
    assert db_manager.connect(), "No se pudo conectar a la base de datos"
    db_manager.clear_tables()
    
    yield db_manager
    
    db_manager.disconnect()
