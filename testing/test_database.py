"""
Test suite para la base de datos INACAP
========================================

Suite completo de tests para verificar:
- Inserciones válidas e inválidas
- Constraints (CASCADE, RESTRICT)
- Integridad referencial
- Datos semilla (seed data)

Ejecutar con:
    python -m pytest testing/test_database.py -v
    
Ejecutar por markers:
    pytest -m valid       # Solo tests de inserciones válidas
    pytest -m invalid     # Solo tests de inserciones inválidas
    pytest -m constraints # Solo tests de CASCADE/RESTRICT
    pytest -m seed        # Solo tests de verificación de seed data

Otros comandos útiles:
    pytest -v --tb=short  # Con traceback corto
    pytest -k "region"    # Solo tests que contienen "region"
    pytest --collect-only # Ver lista de tests sin ejecutar
"""

import pytest
import mysql.connector
from mysql.connector import Error
from datetime import date
import os
from pathlib import Path
import glob

# Cargar variables de entorno desde .env (si existe)
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent.parent / '.env'
    load_dotenv(dotenv_path=env_path)
except ImportError:
    pass

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
            seed_dir = Path(__file__).parent.parent / 'database' / 'seed_data'
            
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
            
            self.cursor.execute("SET FOREIGN_KEY_CHECKS=0")
            
            for seed_file in seed_files:
                file_path = seed_dir / seed_file
                if file_path.exists():
                    with open(file_path, 'r', encoding='utf-8') as f:
                        sql_content = f.read()
                        # Ejecutar todo el contenido como un solo bloque si es posible
                        if sql_content.strip():
                            try:
                                # Limpiar comentarios de línea
                                lines = [line for line in sql_content.split('\n') if not line.strip().startswith('--')]
                                sql_clean = '\n'.join(lines)
                                # Ejecutar el contenido completo
                                for stmt in sql_clean.split(';'):
                                    stmt = stmt.strip()
                                    if stmt:
                                        try:
                                            self.cursor.execute(stmt)
                                        except Error as e:
                                            # Silenciar errores menores
                                            pass
                            except Error as e:
                                print(f"  (Advertencia en {seed_file}: {str(e)[:50]})")
            
            self.cursor.execute("SET FOREIGN_KEY_CHECKS=1")
            self.connection.commit()
            print("✓ Datos semilla cargados exitosamente")
            return True
        except Error as e:
            self.connection.rollback()
            print(f"✗ Error al cargar datos semilla: {e}")
            return False



# ===== FIXTURES =====

@pytest.fixture(scope="function")
def db():
    """Fixture para inicializar BD con datos semilla"""
    db_manager = DatabaseManager()
    assert db_manager.connect(), "No se pudo conectar a la base de datos"
    db_manager.clear_tables()
    db_manager.load_seed_data()  # Cargar seed data automáticamente
    
    yield db_manager
    
    db_manager.disconnect()


@pytest.fixture(scope="function")
def db_empty():
    """Fixture alternativa: BD limpia SIN datos semilla"""
    db_manager = DatabaseManager()
    assert db_manager.connect(), "No se pudo conectar a la base de datos"
    db_manager.clear_tables()
    
    yield db_manager
    
    db_manager.disconnect()


# ===== TESTS DE ESTRUCTURA (SCHEMA VALIDATION) =====

class TestEstructuraBaseDatos:
    """Pruebas de validación de estructura de la base de datos"""
    
    @pytest.mark.valid
    def test_todas_las_tablas_core_se_crean(self, db_empty):
        """Verificar que todas las tablas core se crean correctamente desde los archivos SQL"""
        schema_dir = Path(__file__).parent.parent / 'database' / 'schema' / 'core'
        
        # Lista esperada de tablas core (MySQL las convierte a minúsculas)
        tablas_esperadas = [
            'region', 'area_academica', 'area_conocimiento', 'institucion',
            'comuna', 'direccion', 'ramo', 'profesor', 'colegio', 'estudiante',
            'plan_estudio', 'carrera', 'historialinstitucional', 'prerequisitos',
            'ramos_plan_estudio', 'secciones_ramos', 'predictor_datos', 'matricula',
            'notas_estudiante', 'inscripciones_ramos', 'pago', 'cuota', 'transaccion_pago'
        ]
        
        # Ejecutar todos los archivos SQL del schema core en orden
        archivos_sql = sorted(glob.glob(str(schema_dir / '*.sql')))
        
        for archivo in archivos_sql:
            with open(archivo, 'r', encoding='utf-8') as f:
                sql = f.read()
                # Ejecutar cada statement por separado
                for statement in sql.split(';'):
                    statement = statement.strip()
                    if statement and not statement.startswith('--'):
                        success, error = db_empty.execute_query(statement)
                        if not success and 'already exists' not in str(error).lower():
                            assert success, f"Error al ejecutar {Path(archivo).name}: {error}"
        
        # Verificar que todas las tablas existen
        query = "SHOW TABLES"
        result = db_empty.fetch_query(query)
        tablas_creadas = [row[0] for row in result]
        
        for tabla in tablas_esperadas:
            assert tabla in tablas_creadas, f"Tabla {tabla} no se creó correctamente"
        
        print(f"✓ {len(tablas_creadas)} tablas core creadas exitosamente")
    
    @pytest.mark.valid
    def test_todas_las_tablas_bridge_se_crean(self, db_empty):
        """Verificar que todas las tablas bridge (many-to-many) se crean correctamente"""
        # Primero crear las tablas core necesarias
        schema_core_dir = Path(__file__).parent.parent / 'database' / 'schema' / 'core'
        archivos_core = sorted(glob.glob(str(schema_core_dir / '*.sql')))
        
        for archivo in archivos_core:
            with open(archivo, 'r', encoding='utf-8') as f:
                sql = f.read()
                for statement in sql.split(';'):
                    statement = statement.strip()
                    if statement and not statement.startswith('--'):
                        db_empty.execute_query(statement)
        
        # Ahora crear las tablas bridge
        schema_bridge_dir = Path(__file__).parent.parent / 'database' / 'schema' / 'bridge'
        
        # MySQL convierte nombres a minúsculas
        tablas_bridge_esperadas = [
            'estudiante_colegio',
            'estudiante_direccion',
            'ramo_areaconocimiento',
            'ramos_plan_estudio_prequsito'
        ]
        
        archivos_bridge = sorted(glob.glob(str(schema_bridge_dir / '*.sql')))
        
        for archivo in archivos_bridge:
            with open(archivo, 'r', encoding='utf-8') as f:
                sql = f.read()
                for statement in sql.split(';'):
                    statement = statement.strip()
                    if statement and not statement.startswith('--'):
                        success, error = db_empty.execute_query(statement)
                        if not success and 'already exists' not in str(error).lower():
                            assert success, f"Error al ejecutar {Path(archivo).name}: {error}"
        
        # Verificar que todas las tablas bridge existen
        query = "SHOW TABLES"
        result = db_empty.fetch_query(query)
        tablas_creadas = [row[0] for row in result]
        
        for tabla in tablas_bridge_esperadas:
            assert tabla in tablas_creadas, f"Tabla bridge {tabla} no se creó correctamente"
        
        print(f"✓ {len(tablas_bridge_esperadas)} tablas bridge creadas exitosamente")
    
    @pytest.mark.valid
    def test_verificar_indices_existen(self, db):
        """Verificar que los índices importantes existen en las tablas principales"""
        # Verificar índices UNIQUE en tablas principales (nombres en minúsculas)
        indices_esperados = [
            ('region', 'codigo'),
            ('region', 'nombre'),
            ('estudiante', 'rut'),
            ('estudiante', 'email_institucional'),
            ('colegio', 'rbd'),
            ('profesor', 'rut'),
            ('profesor', 'email_institucional'),
            ('ramo', 'sigla'),
        ]
        
        for tabla, columna in indices_esperados:
            query = f"""
                SELECT COUNT(*) 
                FROM INFORMATION_SCHEMA.STATISTICS 
                WHERE TABLE_SCHEMA = %s 
                AND TABLE_NAME = %s 
                AND COLUMN_NAME = %s
            """
            result = db.fetch_query(query, (DB_NAME, tabla, columna))
            
            assert result and result[0][0] > 0, \
                f"Índice esperado en {tabla}.{columna} no existe"
        
        print(f"✓ Todos los {len(indices_esperados)} índices verificados correctamente")


class TestUniqueConstraints:
    """Pruebas exhaustivas de constraints UNIQUE en todas las tablas"""
    
    @pytest.mark.invalid
    def test_region_codigo_unique(self, db):
        """Region.codigo debe ser UNIQUE (seed tiene código 11)"""
        query = "INSERT INTO Region (codigo, nombre) VALUES (%s, %s)"
        success, _ = db.execute_query(query, (11, 'Nueva Region'))
        assert not success, "Se permitió código de región duplicado"
    
    @pytest.mark.invalid
    def test_region_nombre_unique(self, db):
        """Region.nombre debe ser UNIQUE (seed tiene 'Aysén del General Carlos Ibáñez del Campo')"""
        query = "INSERT INTO Region (codigo, nombre) VALUES (%s, %s)"
        success, _ = db.execute_query(query, (99, 'Aysén del General Carlos Ibáñez del Campo'))
        assert not success, "Se permitió nombre de región duplicado"
    
    @pytest.mark.invalid
    def test_comuna_codigo_unique(self, db):
        """Comuna.codigo debe ser UNIQUE (seed tiene código 11101)"""
        # Obtener una región válida
        row = db.fetch_query("SELECT id_region FROM Region LIMIT 1")
        assert row and row[0], "No hay regiones disponibles"
        id_region = row[0][0]
        
        query = "INSERT INTO Comuna (id_region, codigo, nombre) VALUES (%s, %s, %s)"
        success, _ = db.execute_query(query, (id_region, 11101, 'Comuna Nueva'))
        assert not success, "Se permitió código de comuna duplicado"
    
    @pytest.mark.invalid
    def test_comuna_nombre_region_unique(self, db):
        """Comuna tiene UNIQUE(nombre, id_region) - mismo nombre en misma región"""
        row = db.fetch_query("SELECT id_region FROM Comuna WHERE nombre = %s", ('Coyhaique',))
        assert row and row[0], "Comuna Coyhaique no encontrada"
        id_region = row[0][0]
        
        query = "INSERT INTO Comuna (id_region, codigo, nombre) VALUES (%s, %s, %s)"
        success, _ = db.execute_query(query, (id_region, 99999, 'Coyhaique'))
        assert not success, "Se permitió mismo nombre de comuna en misma región"
    
    @pytest.mark.valid
    def test_comuna_mismo_nombre_diferente_region(self, db):
        """Comuna permite mismo nombre en DIFERENTE región (válido)"""
        # Obtener dos regiones diferentes
        rows = db.fetch_query("SELECT id_region FROM Region LIMIT 2")
        assert rows and len(rows) >= 2, "No hay suficientes regiones"
        id_region_1, id_region_2 = rows[0][0], rows[1][0]
        
        # Insertar comuna en primera región
        query = "INSERT INTO Comuna (id_region, codigo, nombre) VALUES (%s, %s, %s)"
        success, error = db.execute_query(query, (id_region_1, 88888, 'Nombre Compartido'))
        assert success, f"Error al insertar primera comuna: {error}"
        
        # Insertar comuna con mismo nombre en segunda región (debe permitirse)
        success, error = db.execute_query(query, (id_region_2, 88889, 'Nombre Compartido'))
        assert success, f"No se permitió mismo nombre en diferente región: {error}"
    
    @pytest.mark.invalid
    def test_estudiante_rut_unique(self, db):
        """Estudiante.rut debe ser UNIQUE (seed tiene '20587683-9')"""
        query = """
            INSERT INTO Estudiante 
            (rut, nombre, email_institucional, telefono, fecha_nacimiento, edad, sexo, nacionalidad, ano_egreso_media, puntaje_psu, integrantes_grupo_familiar)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        success, _ = db.execute_query(query, (
            '20587683-9', 'Duplicado', 'nuevo@inacapmail.cl', '+569999999',
            date(2005, 1, 1), 21, 'M', 'CHILE', 2023, 500, 3
        ))
        assert not success, "Se permitió RUT de estudiante duplicado"
    
    @pytest.mark.invalid
    def test_estudiante_email_institucional_unique(self, db):
        """Estudiante.email_institucional debe ser UNIQUE (seed tiene 'camila.manriquez07@inacapmail.cl')"""
        query = """
            INSERT INTO Estudiante 
            (rut, nombre, email_institucional, telefono, fecha_nacimiento, edad, sexo, nacionalidad, ano_egreso_media, puntaje_psu, integrantes_grupo_familiar)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        success, _ = db.execute_query(query, (
            '11111111-1', 'Nuevo', 'camila.manriquez07@inacapmail.cl', '+569999999',
            date(2005, 1, 1), 21, 'M', 'CHILE', 2023, 500, 3
        ))
        assert not success, "Se permitió email institucional de estudiante duplicado"
    
    @pytest.mark.invalid
    def test_estudiante_email_personal_unique(self, db):
        """Estudiante.email_personal debe ser UNIQUE si se proporciona"""
        # Primero insertar un estudiante con email personal
        query = """
            INSERT INTO Estudiante 
            (rut, nombre, email_institucional, email_personal, telefono, fecha_nacimiento, edad, sexo, nacionalidad, ano_egreso_media, puntaje_psu, integrantes_grupo_familiar)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        success, error = db.execute_query(query, (
            '22222222-2', 'Primero', 'primero@inacapmail.cl', 'personal@gmail.com', '+569111111',
            date(2005, 1, 1), 21, 'M', 'CHILE', 2023, 500, 3
        ))
        assert success, f"Error al insertar primer estudiante: {error}"
        
        # Intentar insertar otro con mismo email personal
        success, _ = db.execute_query(query, (
            '33333333-3', 'Segundo', 'segundo@inacapmail.cl', 'personal@gmail.com', '+569222222',
            date(2005, 1, 1), 21, 'F', 'CHILE', 2023, 500, 3
        ))
        assert not success, "Se permitió email personal duplicado"
    
    @pytest.mark.invalid
    def test_profesor_rut_unique(self, db):
        """Profesor.rut debe ser UNIQUE (seed tiene '12345678-9')"""
        query = """
            INSERT INTO Profesor (nombre, rut, email_institucional)
            VALUES (%s, %s, %s)
        """
        success, _ = db.execute_query(query, ('Nuevo Profesor', '12345678-9', 'nuevo.profesor@inacap.cl'))
        assert not success, "Se permitió RUT de profesor duplicado"
    
    @pytest.mark.invalid
    def test_profesor_email_institucional_unique(self, db):
        """Profesor.email_institucional debe ser UNIQUE (seed tiene 'pedro.rojas@inacap.cl')"""
        query = """
            INSERT INTO Profesor (nombre, rut, email_institucional)
            VALUES (%s, %s, %s)
        """
        success, _ = db.execute_query(query, ('Nuevo Profesor', '99999999-9', 'pedro.rojas@inacap.cl'))
        assert not success, "Se permitió email institucional de profesor duplicado"
    
    @pytest.mark.invalid
    def test_colegio_rbd_unique(self, db):
        """Colegio.rbd debe ser UNIQUE (seed tiene '24206-3')"""
        row = db.fetch_query("SELECT id_comuna, id_region FROM Comuna LIMIT 1")
        assert row and row[0], "No hay comunas disponibles"
        id_comuna, id_region = row[0]
        
        row = db.fetch_query("SELECT id_direccion FROM Direccion LIMIT 1")
        assert row and row[0], "No hay direcciones disponibles"
        id_direccion = row[0][0]
        
        query = """
            INSERT INTO Colegio (id_comuna, id_region, id_direccion, rbd, nombre, tipo_colegio)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        success, _ = db.execute_query(query, (id_comuna, id_region, id_direccion, '24206-3', 'Nuevo Colegio', 'PARTICULARES PAGADOS'))
        assert not success, "Se permitió RBD de colegio duplicado"
    
    @pytest.mark.invalid
    def test_colegio_nombre_comuna_unique(self, db):
        """Colegio tiene UNIQUE(nombre, id_comuna) - mismo nombre en misma comuna"""
        row = db.fetch_query("SELECT id_comuna, id_region, nombre FROM Colegio LIMIT 1")
        assert row and row[0], "No hay colegios disponibles"
        id_comuna, id_region, nombre_colegio = row[0]
        
        row = db.fetch_query("SELECT id_direccion FROM Direccion WHERE id_comuna = %s LIMIT 1", (id_comuna,))
        assert row and row[0], "No hay direcciones disponibles"
        id_direccion = row[0][0]
        
        query = """
            INSERT INTO Colegio (id_comuna, id_region, id_direccion, rbd, nombre, tipo_colegio)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        success, _ = db.execute_query(query, (id_comuna, id_region, id_direccion, '99999-9', nombre_colegio, 'PARTICULARES PAGADOS'))
        assert not success, "Se permitió mismo nombre de colegio en misma comuna"
    
    @pytest.mark.valid
    def test_colegio_mismo_nombre_diferente_comuna(self, db):
        """Colegio permite mismo nombre en DIFERENTE comuna (válido)"""
        rows = db.fetch_query("SELECT id_comuna, id_region FROM Comuna LIMIT 2")
        assert rows and len(rows) >= 2, "No hay suficientes comunas"
        id_comuna_1, id_region_1 = rows[0]
        id_comuna_2, id_region_2 = rows[1]
        
        # Obtener o crear dirección para comuna 1
        rows = db.fetch_query("SELECT id_direccion FROM Direccion WHERE id_comuna = %s LIMIT 1", (id_comuna_1,))
        if not rows or not rows[0]:
            db.execute_query("INSERT INTO Direccion (id_comuna, calle, numero, tipo_direccion) VALUES (%s, %s, %s, %s)",
                           (id_comuna_1, 'Calle Test 1', 111, 'Permanente'))
            rows = db.fetch_query("SELECT id_direccion FROM Direccion WHERE id_comuna = %s LIMIT 1", (id_comuna_1,))
        id_direccion_1 = rows[0][0]
        
        # Obtener o crear dirección para comuna 2
        rows = db.fetch_query("SELECT id_direccion FROM Direccion WHERE id_comuna = %s LIMIT 1", (id_comuna_2,))
        if not rows or not rows[0]:
            db.execute_query("INSERT INTO Direccion (id_comuna, calle, numero, tipo_direccion) VALUES (%s, %s, %s, %s)",
                           (id_comuna_2, 'Calle Test 2', 222, 'Permanente'))
            rows = db.fetch_query("SELECT id_direccion FROM Direccion WHERE id_comuna = %s LIMIT 1", (id_comuna_2,))
        id_direccion_2 = rows[0][0]
        
        query = """
            INSERT INTO Colegio (id_comuna, id_region, id_direccion, rbd, nombre, tipo_colegio)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        success, error = db.execute_query(query, (id_comuna_1, id_region_1, id_direccion_1, '77777-7', 'Nombre Compartido', 'PARTICULARES PAGADOS'))
        assert success, f"Error al insertar primer colegio: {error}"
        
        success, error = db.execute_query(query, (id_comuna_2, id_region_2, id_direccion_2, '77778-8', 'Nombre Compartido', 'PARTICULARES PAGADOS'))
        assert success, f"No se permitió mismo nombre en diferente comuna: {error}"
    
    @pytest.mark.invalid
    def test_ramo_sigla_unique(self, db):
        """Ramo.sigla debe ser UNIQUE (seed tiene 'MAT101')"""
        query = """
            INSERT INTO Ramo (sigla, nombre_ramo, horas_teoricas, horas_practicas, horas_semanales, nivel_recomendado)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        success, _ = db.execute_query(query, ('MAT101', 'Nuevo Ramo', 2, 2, 4, 1))
        assert not success, "Se permitió sigla de ramo duplicada"
    
    @pytest.mark.invalid
    def test_ramo_sigla_nombre_unique(self, db):
        """Ramo tiene UNIQUE(sigla, nombre_ramo) - misma combinación no permitida"""
        row = db.fetch_query("SELECT sigla, nombre_ramo FROM Ramo LIMIT 1")
        assert row and row[0], "No hay ramos disponibles"
        sigla, nombre = row[0]
        
        query = """
            INSERT INTO Ramo (sigla, nombre_ramo, horas_teoricas, horas_practicas, horas_semanales, nivel_recomendado)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        success, _ = db.execute_query(query, (sigla, nombre, 2, 2, 4, 1))
        assert not success, "Se permitió combinación sigla+nombre duplicada"
    
    @pytest.mark.invalid
    def test_area_academica_nombre_unique(self, db):
        """Area_Academica.nombre_area_academica debe ser UNIQUE (seed tiene 'Salud')"""
        query = "INSERT INTO Area_Academica (nombre_area_academica) VALUES (%s)"
        success, _ = db.execute_query(query, ('Salud',))
        assert not success, "Se permitió nombre de área académica duplicado"
    
    @pytest.mark.invalid
    def test_area_conocimiento_nombre_unique(self, db):
        """Area_Conocimiento.nombre_area_conocimiento debe ser UNIQUE (seed tiene 'Matemáticas')"""
        query = "INSERT INTO Area_Conocimiento (nombre_area_conocimiento, color) VALUES (%s, %s)"
        success, _ = db.execute_query(query, ('Matemáticas', '#FF0000'))
        assert not success, "Se permitió nombre de área de conocimiento duplicado"
    
    @pytest.mark.invalid
    def test_area_conocimiento_color_unique(self, db):
        """Area_Conocimiento.color debe ser UNIQUE (seed tiene '#FF5733')"""
        query = "INSERT INTO Area_Conocimiento (nombre_area_conocimiento, color) VALUES (%s, %s)"
        success, _ = db.execute_query(query, ('Nueva Area', '#FF5733'))
        assert not success, "Se permitió color duplicado en área de conocimiento"
    
    @pytest.mark.invalid
    def test_institucion_nombre_unique(self, db):
        """Institucion.nombre_institucion debe ser UNIQUE (seed tiene 'INACAP Centro de Formación Técnica')"""
        query = "INSERT INTO Institucion (tipo_instucion, nombre_institucion) VALUES (%s, %s)"
        success, _ = db.execute_query(query, ('I:P', 'INACAP Centro de Formación Técnica'))
        assert not success, "Se permitió nombre de institución duplicado"
    
    @pytest.mark.invalid
    def test_institucion_tipo_nombre_unique(self, db):
        """Institucion tiene UNIQUE(tipo_instucion, nombre_institucion)"""
        row = db.fetch_query("SELECT tipo_instucion, nombre_institucion FROM Institucion LIMIT 1")
        assert row and row[0], "No hay instituciones disponibles"
        tipo, nombre = row[0]
        
        query = "INSERT INTO Institucion (tipo_instucion, nombre_institucion) VALUES (%s, %s)"
        success, _ = db.execute_query(query, (tipo, nombre))
        assert not success, "Se permitió combinación tipo+nombre duplicada en institución"
    
    @pytest.mark.invalid
    def test_carrera_codigo_unique(self, db):
        """Carrera.codigo_carrera debe ser UNIQUE (seed tiene 'AE')"""
        row = db.fetch_query("SELECT id_area_academica, id_institucion, id_plan_estudio FROM Carrera LIMIT 1")
        assert row and row[0], "No hay carreras disponibles"
        id_area, id_inst, id_plan = row[0]
        
        query = """
            INSERT INTO Carrera (id_area_academica, id_institucion, id_plan_estudio, codigo_carrera, nombre_carrera, jornada, tipo_programa)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        success, _ = db.execute_query(query, (id_area, id_inst, id_plan, 'AE', 'Nueva Carrera', 'DIURNA', 'REGULAR'))
        assert not success, "Se permitió código de carrera duplicado"
    
    @pytest.mark.invalid
    def test_carrera_nombre_unique(self, db):
        """Carrera.nombre_carrera debe ser UNIQUE (seed tiene 'Administración de Empresas')"""
        row = db.fetch_query("SELECT id_area_academica, id_institucion, id_plan_estudio FROM Carrera LIMIT 1")
        assert row and row[0], "No hay carreras disponibles"
        id_area, id_inst, id_plan = row[0]
        
        query = """
            INSERT INTO Carrera (id_area_academica, id_institucion, id_plan_estudio, codigo_carrera, nombre_carrera, jornada, tipo_programa)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        success, _ = db.execute_query(query, (id_area, id_inst, id_plan, 'ZZZZ', 'Administración de Empresas', 'DIURNA', 'REGULAR'))
        assert not success, "Se permitió nombre de carrera duplicado"


class TestInsertarDatosValidos:
    """Pruebas de inserciones válidas usando datos semilla"""
    
    @pytest.mark.seed
    def test_verificar_datos_semilla(self, db):
        """Verificar que los datos semilla se cargaron correctamente"""
        result = db.fetch_query("SELECT COUNT(*) FROM Region")
        assert result[0][0] >= 4, "No se cargaron las regiones semilla"
        
        result = db.fetch_query("SELECT COUNT(*) FROM Estudiante")
        assert result[0][0] >= 8, "No se cargaron los estudiantes semilla"
    
    @pytest.mark.valid
    def test_insertar_region_nueva(self, db):
        """Insertar una región nueva adicional a la semilla"""
        query = "INSERT INTO Region (codigo, nombre) VALUES (%s, %s)"
        success, error = db.execute_query(query, (10, 'Los Lagos'))
        
        assert success, f"Error al insertar región: {error}"
        
        result = db.fetch_query("SELECT * FROM Region WHERE codigo = 10")
        assert result and len(result) > 0, "Región no encontrada después de insertar"
    
    @pytest.mark.valid
    def test_insertar_multiple_regiones(self, db):
        """Insertar múltiples regiones nuevas"""
        regions = [(10, 'Los Lagos'), (14, 'Los Ríos'), (15, 'Arica y Parinacota')]
        
        for codigo, nombre in regions:
            query = "INSERT INTO Region (codigo, nombre) VALUES (%s, %s)"
            success, error = db.execute_query(query, (codigo, nombre))
            assert success, f"Error al insertar región {nombre}: {error}"
        
        result = db.fetch_query("SELECT COUNT(*) FROM Region")
        assert result[0][0] >= 7, "No se insertaron todas las regiones"
    
    @pytest.mark.valid
    def test_insertar_estudiante_nuevo(self, db):
        """Insertar un estudiante nuevo adicional a la semilla"""
        query = (
            "INSERT INTO Estudiante "
            "(rut, nombre, email_institucional, telefono, fecha_nacimiento, edad, sexo, nacionalidad, ano_egreso_media, puntaje_psu, integrantes_grupo_familiar) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        )
        
        success, error = db.execute_query(
            query,
            (
                '99999999-9',
                'Test Usuario Nuevo',
                'test.nuevo@inacapmail.cl',
                '+569999999999',
                date(2005, 6, 20),
                20,
                'M',
                'CHILE',
                2023,
                580,
                3,
            ),
        )
        
        assert success, f"Error al insertar estudiante: {error}"
        
        result = db.fetch_query("SELECT COUNT(*) FROM Estudiante WHERE rut = %s", ('99999999-9',))
        assert result[0][0] == 1, "Estudiante no encontrado"
    
    @pytest.mark.valid
    def test_usar_datos_semilla_para_colegio(self, db):
        """Usar comuna de semilla para insertar colegio nuevo"""
        row = db.fetch_query("SELECT id_comuna, id_region FROM Comuna WHERE nombre = %s", ('Coyhaique',))
        assert row and row[0], "Comuna Coyhaique no encontrada"
        id_comuna, id_region = row[0]
        
        row = db.fetch_query("SELECT id_direccion FROM Direccion WHERE id_comuna = %s LIMIT 1", (id_comuna,))
        assert row and row[0], "Dirección no encontrada"
        id_direccion = row[0][0]
        
        query = (
            "INSERT INTO Colegio (id_comuna, id_region, id_direccion, rbd, nombre, tipo_colegio) "
            "VALUES (%s, %s, %s, %s, %s, %s)"
        )
        success, error = db.execute_query(
            query, (id_comuna, id_region, id_direccion, '99999-9', 'Colegio Test Nuevo', 'PARTICULARES PAGADOS')
        )
        
        assert success, f"Error al insertar colegio: {error}"


class TestInsertarDatosInvalidos:
    """Pruebas de inserciones inválidas usando datos semilla"""
    
    @pytest.mark.invalid
    def test_region_codigo_duplicado(self, db):
        """No permitir códigos de región duplicados (seed tiene código 11)"""
        query = "INSERT INTO Region (codigo, nombre) VALUES (%s, %s)"
        success, _ = db.execute_query(query, (11, 'Otra Región'))
        assert not success, "Se permitió insertar región con código duplicado"
    
    @pytest.mark.invalid
    def test_region_nombre_duplicado(self, db):
        """No permitir nombres de región duplicados"""
        query = "INSERT INTO Region (codigo, nombre) VALUES (%s, %s)"
        success, _ = db.execute_query(query, (99, 'Aysén del General Carlos Ibáñez del Campo'))
        assert not success, "Se permitió insertar región con nombre duplicado"
    
    @pytest.mark.invalid
    def test_comuna_sin_region_valida(self, db):
        """No permitir comuna con región inexistente"""
        query = "INSERT INTO Comuna (id_region, codigo, nombre) VALUES (%s, %s, %s)"
        success, error = db.execute_query(query, (999, 1001, 'Coyhaique'))
        assert not success, "Se permitió insertar comuna sin región válida"
        assert error and ("FOREIGN KEY" in error or "foreign key" in error.lower())
    
    @pytest.mark.invalid
    def test_colegio_rbd_duplicado(self, db):
        """No permitir RBD duplicado en Colegio (seed tiene '24206-3')"""
        row = db.fetch_query("SELECT id_comuna, id_region FROM Comuna WHERE nombre = %s", ('Coyhaique',))
        assert row and row[0], "Comuna no encontrada"
        id_comuna, id_region = row[0]
        
        row = db.fetch_query("SELECT id_direccion FROM Direccion WHERE id_comuna = %s LIMIT 1", (id_comuna,))
        assert row and row[0], "Dirección no encontrada"
        id_direccion = row[0][0]
        
        query = (
            "INSERT INTO Colegio (id_comuna, id_region, id_direccion, rbd, nombre, tipo_colegio) "
            "VALUES (%s, %s, %s, %s, %s, %s)"
        )
        success, _ = db.execute_query(query, (id_comuna, id_region, id_direccion, '24206-3', 'Colegio Duplicado', 'PARTICULARES SUBVENCIONADOS'))
        assert not success, "Se permitió insertar colegio con RBD duplicado"
    
    @pytest.mark.invalid
    def test_estudiante_email_duplicado(self, db):
        """No permitir emails institucionales duplicados (seed tiene datos)"""
        query = (
            "INSERT INTO Estudiante "
            "(rut, nombre, email_institucional, telefono, fecha_nacimiento, edad, sexo, nacionalidad, ano_egreso_media, puntaje_psu, integrantes_grupo_familiar) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        )
        success, _ = db.execute_query(
            query,
            (
                '99888777-6',
                'Otro Usuario',
                'camila.manriquez07@inacapmail.cl',  # Email presente en seed
                '+569738539999',
                date(2005, 3, 15),
                20,
                'M',
                'CHILE',
                2022,
                550,
                4,
            ),
        )
        assert not success, "Se permitió insertar estudiante con email duplicado"
    
    @pytest.mark.invalid
    def test_estudiante_rut_duplicado(self, db):
        """No permitir RUT duplicado (seed tiene '20587683-9')"""
        query = (
            "INSERT INTO Estudiante "
            "(rut, nombre, email_institucional, telefono, fecha_nacimiento, edad, sexo, nacionalidad, ano_egreso_media, puntaje_psu, integrantes_grupo_familiar) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        )
        success, _ = db.execute_query(
            query,
            (
                '20587683-9',  # RUT presente en seed
                'Duplicado',
                'nuevo.email@inacapmail.cl',
                '+569700000000',
                date(2004, 3, 15),
                21,
                'F',
                'CHILE',
                2022,
                550,
                4,
            ),
        )
        assert not success, "Se permitió insertar estudiante con RUT duplicado"


class TestConstraintsCascadeRestrict:
    """Pruebas de CASCADE y RESTRICT con datos semilla"""
    
    @pytest.mark.constraints
    def test_restrict_eliminar_region_con_comunas(self, db):
        """No se puede eliminar región que tiene comunas (RESTRICT)"""
        row = db.fetch_query("SELECT id_region FROM Region WHERE codigo = %s", (11,))
        assert row and row[0], "Región 11 no encontrada"
        id_region = row[0][0]
        
        success, error = db.execute_query("DELETE FROM Region WHERE id_region = %s", (id_region,))
        assert not success, "Se permitió eliminar región con comunas"
        assert error and ("FOREIGN KEY" in error or "restrict" in error.lower())
        
        row = db.fetch_query("SELECT COUNT(*) FROM Region WHERE id_region = %s", (id_region,))
        assert row[0][0] == 1, "La región fue eliminada indebidamente"
    
    @pytest.mark.constraints
    def test_restrict_eliminar_comuna_con_colegios(self, db):
        """No se puede eliminar comuna que tiene colegios (RESTRICT)"""
        row = db.fetch_query("SELECT id_comuna FROM Comuna WHERE nombre = %s", ('Coyhaique',))
        assert row and row[0], "Comuna Coyhaique no encontrada"
        id_comuna = row[0][0]
        
        success, _ = db.execute_query("DELETE FROM Comuna WHERE id_comuna = %s", (id_comuna,))
        assert not success, "Se permitió eliminar comuna con colegios"
        
        row = db.fetch_query("SELECT COUNT(*) FROM Comuna WHERE id_comuna = %s", (id_comuna,))
        assert row[0][0] == 1, "La comuna fue eliminada indebidamente"
    
    @pytest.mark.constraints
    def test_cascade_eliminar_estudiante_elimina_historial(self, db):
        """Al eliminar estudiante se elimina su historial (CASCADE)"""
        row = db.fetch_query("SELECT id_estudiante FROM Estudiante WHERE rut = %s", ('20587683-9',))
        assert row and row[0], "Camila no encontrada"
        est_id = row[0][0]
        
        antes = db.fetch_query("SELECT COUNT(*) FROM HistorialInstitucional WHERE id_estudiante = %s", (est_id,))
        assert antes[0][0] > 0, "Camila no tiene historial en seed"
        
        success, error = db.execute_query("DELETE FROM Estudiante WHERE id_estudiante = %s", (est_id,))
        assert success, f"Error al eliminar estudiante: {error}"
        
        despues = db.fetch_query("SELECT COUNT(*) FROM HistorialInstitucional WHERE id_estudiante = %s", (est_id,))
        assert despues[0][0] == 0, "Historial no eliminado por CASCADE"
    
    @pytest.mark.constraints
    def test_cascade_eliminar_estudiante_elimina_relaciones(self, db):
        """Al eliminar estudiante se eliminan relaciones en tablas puente (CASCADE)"""
        row = db.fetch_query("SELECT id_estudiante FROM Estudiante WHERE rut = %s", ('20587683-9',))
        assert row and row[0], "Camila no encontrada"
        est_id = row[0][0]
        
        # Verificar relaciones previas en seed
        ed_antes = db.fetch_query("SELECT COUNT(*) FROM estudiante_direccion WHERE id_estudiante = %s", (est_id,))
        assert ed_antes[0][0] >= 1, "Camila no tiene dirección en seed"
        
        success, error = db.execute_query("DELETE FROM Estudiante WHERE id_estudiante = %s", (est_id,))
        assert success, f"Error al eliminar estudiante: {error}"
        
        ed_despues = db.fetch_query("SELECT COUNT(*) FROM estudiante_direccion WHERE id_estudiante = %s", (est_id,))
        assert ed_despues[0][0] == 0, "Relación estudiante_direccion no se eliminó por CASCADE"
    
    @pytest.mark.constraints
    def test_restrict_eliminar_colegio_con_estudiantes(self, db):
        """No se puede eliminar colegio con estudiantes asociados (RESTRICT)"""
        row = db.fetch_query("SELECT id_colegio FROM Colegio WHERE rbd = %s", ('24206-3',))
        assert row and row[0], "Colegio con RBD 24206-3 no encontrado"
        id_colegio = row[0][0]
        
        success, _ = db.execute_query("DELETE FROM Colegio WHERE id_colegio = %s", (id_colegio,))
        assert not success, "Se permitió eliminar colegio con estudiantes asociados"
        
        row = db.fetch_query("SELECT COUNT(*) FROM Colegio WHERE id_colegio = %s", (id_colegio,))
        assert row[0][0] == 1, "El colegio fue eliminado indebidamente"
    
    @pytest.mark.constraints
    def test_cascade_eliminar_direccion_elimina_relacion(self, db):
        """Al eliminar dirección sin referencias en Colegio se elimina relación (CASCADE)"""
        # Crear una dirección nueva SIN referencias en Colegio
        row = db.fetch_query("SELECT id_comuna FROM Comuna WHERE nombre = %s", ('Coyhaique',))
        assert row and row[0], "Comuna no encontrada"
        id_comuna = row[0][0]
        
        success, error = db.execute_query(
            "INSERT INTO Direccion (id_comuna, calle, numero, tipo_direccion) VALUES (%s, %s, %s, %s)",
            (id_comuna, 'Calle Test Única', 999, 'Permanente')
        )
        assert success, f"Error al insertar dirección: {error}"
        
        # Obtener el ID de la nueva dirección
        row = db.fetch_query("SELECT id_direccion FROM Direccion WHERE calle = %s", ('Calle Test Única',))
        assert row and row[0], "Dirección creada no encontrada"
        id_direccion = row[0][0]
        
        # Buscar un estudiante que podamos vincular a esta dirección
        row = db.fetch_query("SELECT id_estudiante FROM Estudiante LIMIT 1")
        assert row and row[0], "No hay estudiante disponible"
        id_estudiante = row[0][0]
        
        # Vincular estudiante a la dirección
        success, error = db.execute_query(
            "INSERT INTO estudiante_direccion (id_estudiante, id_direccion) VALUES (%s, %s)",
            (id_estudiante, id_direccion)
        )
        assert success, f"Error al vincular dirección: {error}"
        
        # Verificar que existe la relación
        row = db.fetch_query("SELECT COUNT(*) FROM estudiante_direccion WHERE id_direccion = %s", (id_direccion,))
        assert row[0][0] >= 1, "Relación no se creó"
        
        # Ahora sí, eliminar la dirección
        success, error = db.execute_query("DELETE FROM Direccion WHERE id_direccion = %s", (id_direccion,))
        assert success, f"Error al eliminar dirección: {error}"
        
        # Verificar que la relación se eliminó por CASCADE
        row = db.fetch_query("SELECT COUNT(*) FROM estudiante_direccion WHERE id_direccion = %s", (id_direccion,))
        assert row[0][0] == 0, "Relación no se eliminó por CASCADE"


if __name__ == "__main__":
    """
    Ejecutar con: python -m pytest test_database.py -v
    O: pytest test_database.py -v -s (con salida detallada)
    """
    pytest.main([__file__, "-v", "-s"])
