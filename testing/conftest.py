"""
conftest.py - Configuración compartida para todos los tests
Contiene: DatabaseManager + pytest fixtures + markers
"""

import pytest
import mysql.connector
from mysql.connector import Error
import os
from pathlib import Path


def pytest_configure(config):
    """Configurar markers personalizados para pytest"""
    config.addinivalue_line("markers", "valid: Tests para inserciones válidas")
    config.addinivalue_line("markers", "invalid: Tests para inserciones inválidas (deben fallar)")
    config.addinivalue_line("markers", "constraints: Tests de CASCADE y RESTRICT")
    config.addinivalue_line("markers", "seed: Tests de verificación de datos semilla")
    config.addinivalue_line("markers", "slow: Tests que toman más tiempo en ejecutar")

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
            
            # Obtener todas las tablas de la BD
            self.cursor.execute("SHOW TABLES")
            tables = [table[0] for table in self.cursor.fetchall()]
            
            # Truncar todas las tablas
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
    
    def load_seed_data(self):
        """Cargar datos semilla desde archivos SQL"""
        try:
            # Ruta al directorio de seed data
            seed_dir = Path(__file__).parent.parent / 'database' / 'seed_data'
            
            # Archivos de seed data en orden
            seed_files = [
                '01_region.sql',
                '02_area_academica.sql',
                '03_area_conocimiento.sql',
                '04_institucion.sql',
                '05_comuna.sql',
                '06_direccion.sql',
                '07_ramo.sql',
                '08_profesor.sql',
                '09_colegio.sql',
                '10_estudiante.sql',
                '11_plan_estudio.sql',
                '12_carrera.sql',
                '13_historial_institucional.sql',
                '14_prerequisitos.sql',
                '15_ramos_plan_estudio.sql',
                '16_secciones_ramos.sql',
                '18_matricula.sql',
                '17_predictor_datos.sql',
                '19_notas_estudiante.sql',
                '20_inscripciones_ramos.sql',
                '21_pagos.sql',
                '22_cuota.sql',
                '23_transaccion_pago.sql',
                '24_estudiante_colegio.sql',
                '25_estudiante_direccion.sql',
                '26_ramo_areaConocimiento.sql',
                '27_ramosPlanEstudio_prerequisito.sql',
            ]
            
            # Deshabilitar constraint checks temporalmente
            self.cursor.execute("SET FOREIGN_KEY_CHECKS=0")
            
            # Cargar cada archivo
            for seed_file in seed_files:
                file_path = seed_dir / seed_file
                if file_path.exists():
                    with open(file_path, 'r', encoding='utf-8') as f:
                        sql_content = f.read()
                        
                        # Ejecutar cada statement SQL
                        for statement in sql_content.split(';'):
                            statement = statement.strip()
                            if statement and not statement.startswith('--'):
                                try:
                                    self.cursor.execute(statement)
                                except Error as e:
                                    # Ignorar errores menores (comentarios, etc)
                                    if 'syntax' not in str(e).lower():
                                        pass
            
            # Reabilitar constraint checks
            self.cursor.execute("SET FOREIGN_KEY_CHECKS=1")
            self.connection.commit()
            print("✓ Datos semilla cargados exitosamente")
            return True
        except Error as e:
            self.connection.rollback()
            print(f"✗ Error al cargar datos semilla: {e}")
            return False


# ===== PYTEST FIXTURE =====

@pytest.fixture(scope="function")
def db():
    """
    Fixture para inicializar BD con datos semilla
    
    Esta fixture:
    1. Conecta a la base de datos
    2. Limpia todas las tablas
    3. Carga datos semilla automáticamente
    4. Proporciona el DatabaseManager para el test
    5. Desconecta al finalizar
    """
    db_manager = DatabaseManager()
    assert db_manager.connect(), "No se pudo conectar a la base de datos"
    db_manager.clear_tables()
    db_manager.load_seed_data()  # ← Carga automática de datos semilla
    
    yield db_manager
    
    db_manager.disconnect()


@pytest.fixture(scope="function")
def db_empty():
    """
    Fixture alternativa: BD limpia SIN datos semilla
    
    Usar cuando necesites una BD completamente vacía.
    Ejemplo: @pytest.mark.usefixtures("db_empty")
    """
    db_manager = DatabaseManager()
    assert db_manager.connect(), "No se pudo conectar a la base de datos"
    db_manager.clear_tables()
    # NO carga datos semilla
    
    yield db_manager
    
    db_manager.disconnect()
