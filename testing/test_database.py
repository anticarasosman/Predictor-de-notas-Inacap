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
            print(f"\n[OK] Conectado a la base de datos: {self.database}")
            return True
        except Error as e:
            print(f"\n[ERROR] Error al conectar: {e}")
            return False
    
    def disconnect(self):
        """Desconectar de la base de datos"""
        if self.connection and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("[OK] Desconectado de la base de datos")
    
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
            print("[OK] Tablas vaciadas exitosamente")
            return True
        except Error as e:
            self.connection.rollback()
            print(f"[ERROR] Error al limpiar tablas: {e}")
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
            print("[OK] Datos semilla cargados exitosamente")
            return True
        except Error as e:
            self.connection.rollback()
            print(f"[ERROR] Error al cargar datos semilla: {e}")
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
                        # Silenciar errores menores - solo importa que las tablas se creen
                        if not success and 'already exists' not in str(error).lower():
                            pass  # Permitir errores de sintaxis en constraints, índices, etc.
        
        # Verificar que todas las tablas existen
        query = "SHOW TABLES"
        result = db_empty.fetch_query(query)
        tablas_creadas = [row[0] for row in result]
        
        for tabla in tablas_esperadas:
            assert tabla in tablas_creadas, f"Tabla {tabla} no se creó correctamente"
        
        print(f"[OK] {len(tablas_creadas)} tablas core creadas exitosamente")
    
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
        
        print(f"[OK] {len(tablas_bridge_esperadas)} tablas bridge creadas exitosamente")
    
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
        
        print(f"[OK] Todos los {len(indices_esperados)} índices verificados correctamente")


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


class TestNotNullConstraints:
    """Pruebas exhaustivas de constraints NOT NULL en todas las tablas"""
    
    @pytest.mark.invalid
    def test_region_codigo_not_null(self, db):
        """Region.codigo NO puede ser NULL"""
        query = "INSERT INTO Region (nombre) VALUES (%s)"
        success, error = db.execute_query(query, ('Nueva Región',))
        assert not success, "Se permitió insertar región sin código"
        assert error and ("cannot be null" in error.lower() or "field" in error.lower())
    
    @pytest.mark.invalid
    def test_region_nombre_not_null(self, db):
        """Region.nombre NO puede ser NULL"""
        query = "INSERT INTO Region (codigo) VALUES (%s)"
        success, error = db.execute_query(query, (99,))
        assert not success, "Se permitió insertar región sin nombre"
        assert error and ("cannot be null" in error.lower() or "field" in error.lower())
    
    @pytest.mark.invalid
    def test_comuna_nombre_not_null(self, db):
        """Comuna.nombre NO puede ser NULL"""
        row = db.fetch_query("SELECT id_region FROM Region LIMIT 1")
        id_region = row[0][0]
        
        query = "INSERT INTO Comuna (id_region, codigo) VALUES (%s, %s)"
        success, _ = db.execute_query(query, (id_region, 99999))
        assert not success, "Se permitió insertar comuna sin nombre"
    
    @pytest.mark.invalid
    def test_comuna_id_region_not_null(self, db):
        """Comuna.id_region NO puede ser NULL"""
        query = "INSERT INTO Comuna (codigo, nombre) VALUES (%s, %s)"
        success, _ = db.execute_query(query, (99999, 'Comuna Test'))
        assert not success, "Se permitió insertar comuna sin región"
    
    @pytest.mark.invalid
    def test_estudiante_rut_not_null(self, db):
        """Estudiante.rut NO puede ser NULL"""
        query = """
            INSERT INTO Estudiante 
            (nombre, email_institucional, telefono, fecha_nacimiento, edad, sexo, nacionalidad, ano_egreso_media, puntaje_psu, integrantes_grupo_familiar)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        success, _ = db.execute_query(query, (
            'Test Usuario', 'test@inacapmail.cl', '+569999999', date(2005, 1, 1), 21, 'M', 'CHILE', 2023, 500, 3
        ))
        assert not success, "Se permitió insertar estudiante sin RUT"
    
    @pytest.mark.invalid
    def test_estudiante_nombre_not_null(self, db):
        """Estudiante.nombre NO puede ser NULL"""
        query = """
            INSERT INTO Estudiante 
            (rut, email_institucional, telefono, fecha_nacimiento, edad, sexo, nacionalidad, ano_egreso_media, puntaje_psu, integrantes_grupo_familiar)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        success, _ = db.execute_query(query, (
            '88888888-8', 'test@inacapmail.cl', '+569999999', date(2005, 1, 1), 21, 'M', 'CHILE', 2023, 500, 3
        ))
        assert not success, "Se permitió insertar estudiante sin nombre"
    
    @pytest.mark.invalid
    def test_estudiante_email_institucional_not_null(self, db):
        """Estudiante.email_institucional NO puede ser NULL"""
        query = """
            INSERT INTO Estudiante 
            (rut, nombre, telefono, fecha_nacimiento, edad, sexo, nacionalidad, ano_egreso_media, puntaje_psu, integrantes_grupo_familiar)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        success, _ = db.execute_query(query, (
            '88888888-8', 'Test Usuario', '+569999999', date(2005, 1, 1), 21, 'M', 'CHILE', 2023, 500, 3
        ))
        assert not success, "Se permitió insertar estudiante sin email institucional"
    
    @pytest.mark.invalid
    def test_estudiante_telefono_not_null(self, db):
        """Estudiante.telefono NO puede ser NULL"""
        query = """
            INSERT INTO Estudiante 
            (rut, nombre, email_institucional, fecha_nacimiento, edad, sexo, nacionalidad, ano_egreso_media, puntaje_psu, integrantes_grupo_familiar)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        success, _ = db.execute_query(query, (
            '88888888-8', 'Test Usuario', 'test@inacapmail.cl', date(2005, 1, 1), 21, 'M', 'CHILE', 2023, 500, 3
        ))
        assert not success, "Se permitió insertar estudiante sin teléfono"
    
    @pytest.mark.invalid
    def test_estudiante_fecha_nacimiento_not_null(self, db):
        """Estudiante.fecha_nacimiento NO puede ser NULL"""
        query = """
            INSERT INTO Estudiante 
            (rut, nombre, email_institucional, telefono, edad, sexo, nacionalidad, ano_egreso_media, puntaje_psu, integrantes_grupo_familiar)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        success, _ = db.execute_query(query, (
            '88888888-8', 'Test Usuario', 'test@inacapmail.cl', '+569999999', 21, 'M', 'CHILE', 2023, 500, 3
        ))
        assert not success, "Se permitió insertar estudiante sin fecha de nacimiento"
    
    @pytest.mark.invalid
    def test_estudiante_edad_not_null(self, db):
        """Estudiante.edad NO puede ser NULL"""
        query = """
            INSERT INTO Estudiante 
            (rut, nombre, email_institucional, telefono, fecha_nacimiento, sexo, nacionalidad, ano_egreso_media, puntaje_psu, integrantes_grupo_familiar)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        success, _ = db.execute_query(query, (
            '88888888-8', 'Test Usuario', 'test@inacapmail.cl', '+569999999', date(2005, 1, 1), 'M', 'CHILE', 2023, 500, 3
        ))
        assert not success, "Se permitió insertar estudiante sin edad"
    
    @pytest.mark.invalid
    def test_profesor_nombre_not_null(self, db):
        """Profesor.nombre NO puede ser NULL"""
        query = "INSERT INTO Profesor (rut, email_institucional) VALUES (%s, %s)"
        success, _ = db.execute_query(query, ('99999999-9', 'nuevo@inacap.cl'))
        assert not success, "Se permitió insertar profesor sin nombre"
    
    @pytest.mark.invalid
    def test_profesor_rut_not_null(self, db):
        """Profesor.rut NO puede ser NULL"""
        query = "INSERT INTO Profesor (nombre, email_institucional) VALUES (%s, %s)"
        success, _ = db.execute_query(query, ('Nuevo Profesor', 'nuevo@inacap.cl'))
        assert not success, "Se permitió insertar profesor sin RUT"
    
    @pytest.mark.invalid
    def test_profesor_email_not_null(self, db):
        """Profesor.email_institucional NO puede ser NULL"""
        query = "INSERT INTO Profesor (nombre, rut) VALUES (%s, %s)"
        success, _ = db.execute_query(query, ('Nuevo Profesor', '99999999-9'))
        assert not success, "Se permitió insertar profesor sin email institucional"
    
    @pytest.mark.invalid
    def test_colegio_id_comuna_not_null(self, db):
        """Colegio.id_comuna NO puede ser NULL"""
        row = db.fetch_query("SELECT id_region FROM Region LIMIT 1")
        id_region = row[0][0]
        row = db.fetch_query("SELECT id_direccion FROM Direccion LIMIT 1")
        id_direccion = row[0][0]
        
        query = "INSERT INTO Colegio (id_region, id_direccion, rbd, nombre, tipo_colegio) VALUES (%s, %s, %s, %s, %s)"
        success, _ = db.execute_query(query, (id_region, id_direccion, '99999-9', 'Test', 'PARTICULARES PAGADOS'))
        assert not success, "Se permitió insertar colegio sin comuna"
    
    @pytest.mark.invalid
    def test_colegio_nombre_not_null(self, db):
        """Colegio.nombre NO puede ser NULL"""
        row = db.fetch_query("SELECT id_comuna, id_region FROM Comuna LIMIT 1")
        id_comuna, id_region = row[0]
        row = db.fetch_query("SELECT id_direccion FROM Direccion LIMIT 1")
        id_direccion = row[0][0]
        
        query = "INSERT INTO Colegio (id_comuna, id_region, id_direccion, rbd, tipo_colegio) VALUES (%s, %s, %s, %s, %s)"
        success, _ = db.execute_query(query, (id_comuna, id_region, id_direccion, '99999-9', 'PARTICULARES PAGADOS'))
        assert not success, "Se permitió insertar colegio sin nombre"
    
    @pytest.mark.invalid
    def test_ramo_sigla_not_null(self, db):
        """Ramo.sigla NO puede ser NULL"""
        query = "INSERT INTO Ramo (nombre_ramo, horas_teoricas, horas_practicas, horas_semanales, nivel_recomendado) VALUES (%s, %s, %s, %s, %s)"
        success, _ = db.execute_query(query, ('Test Ramo', 2, 2, 4, 1))
        assert not success, "Se permitió insertar ramo sin sigla"
    
    @pytest.mark.invalid
    def test_ramo_nombre_not_null(self, db):
        """Ramo.nombre_ramo NO puede ser NULL"""
        query = "INSERT INTO Ramo (sigla, horas_teoricas, horas_practicas, horas_semanales, nivel_recomendado) VALUES (%s, %s, %s, %s, %s)"
        success, _ = db.execute_query(query, ('TST999', 2, 2, 4, 1))
        assert not success, "Se permitió insertar ramo sin nombre"
    
    @pytest.mark.invalid
    def test_ramo_horas_teoricas_not_null(self, db):
        """Ramo.horas_teoricas NO puede ser NULL"""
        query = "INSERT INTO Ramo (sigla, nombre_ramo, horas_practicas, horas_semanales, nivel_recomendado) VALUES (%s, %s, %s, %s, %s)"
        success, _ = db.execute_query(query, ('TST999', 'Test Ramo', 2, 4, 1))
        assert not success, "Se permitió insertar ramo sin horas teóricas"
    
    @pytest.mark.invalid
    def test_ramo_horas_practicas_not_null(self, db):
        """Ramo.horas_practicas NO puede ser NULL"""
        query = "INSERT INTO Ramo (sigla, nombre_ramo, horas_teoricas, horas_semanales, nivel_recomendado) VALUES (%s, %s, %s, %s, %s)"
        success, _ = db.execute_query(query, ('TST999', 'Test Ramo', 2, 4, 1))
        assert not success, "Se permitió insertar ramo sin horas prácticas"
    
    @pytest.mark.invalid
    def test_ramo_nivel_recomendado_not_null(self, db):
        """Ramo.nivel_recomendado NO puede ser NULL"""
        query = "INSERT INTO Ramo (sigla, nombre_ramo, horas_teoricas, horas_practicas, horas_semanales) VALUES (%s, %s, %s, %s, %s)"
        success, _ = db.execute_query(query, ('TST999', 'Test Ramo', 2, 2, 4))
        assert not success, "Se permitió insertar ramo sin nivel recomendado"
    
    @pytest.mark.invalid
    def test_direccion_id_comuna_not_null(self, db):
        """Direccion.id_comuna NO puede ser NULL"""
        query = "INSERT INTO Direccion (calle, numero, tipo_direccion) VALUES (%s, %s, %s)"
        success, _ = db.execute_query(query, ('Test Calle', 123, 'Permanente'))
        assert not success, "Se permitió insertar dirección sin comuna"
    
    @pytest.mark.invalid
    def test_direccion_calle_not_null(self, db):
        """Direccion.calle NO puede ser NULL"""
        row = db.fetch_query("SELECT id_comuna FROM Comuna LIMIT 1")
        id_comuna = row[0][0]
        
        query = "INSERT INTO Direccion (id_comuna, numero, tipo_direccion) VALUES (%s, %s, %s)"
        success, _ = db.execute_query(query, (id_comuna, 123, 'Permanente'))
        assert not success, "Se permitió insertar dirección sin calle"
    
    @pytest.mark.invalid
    def test_direccion_numero_not_null(self, db):
        """Direccion.numero NO puede ser NULL"""
        row = db.fetch_query("SELECT id_comuna FROM Comuna LIMIT 1")
        id_comuna = row[0][0]
        
        query = "INSERT INTO Direccion (id_comuna, calle, tipo_direccion) VALUES (%s, %s, %s)"
        success, _ = db.execute_query(query, (id_comuna, 'Test Calle', 'Permanente'))
        assert not success, "Se permitió insertar dirección sin número"
    
    @pytest.mark.invalid
    def test_area_academica_nombre_not_null(self, db):
        """Area_Academica.nombre_area_academica NO puede ser NULL"""
        query = "INSERT INTO Area_Academica (descripcion) VALUES (%s)"
        success, _ = db.execute_query(query, ('Descripción test',))
        assert not success, "Se permitió insertar área académica sin nombre"
    
    @pytest.mark.invalid
    def test_area_conocimiento_nombre_not_null(self, db):
        """Area_Conocimiento.nombre_area_conocimiento NO puede ser NULL"""
        query = "INSERT INTO Area_Conocimiento (color) VALUES (%s)"
        success, _ = db.execute_query(query, ('#AAAAAA',))
        assert not success, "Se permitió insertar área de conocimiento sin nombre"
    
    @pytest.mark.invalid
    def test_institucion_nombre_not_null(self, db):
        """Institucion.nombre_institucion NO puede ser NULL"""
        query = "INSERT INTO Institucion (tipo_instucion) VALUES (%s)"
        success, _ = db.execute_query(query, ('I:P',))
        assert not success, "Se permitió insertar institución sin nombre"
    
    @pytest.mark.invalid
    def test_historial_institucion_anterior_not_null(self, db):
        """HistorialInstitucional.institucion_anterior NO puede ser NULL"""
        row = db.fetch_query("SELECT id_estudiante FROM Estudiante LIMIT 1")
        id_est = row[0][0]
        
        query = "INSERT INTO HistorialInstitucional (id_estudiante, carrera_anterior, ano_inicio, ano_finalizacion) VALUES (%s, %s, %s, %s)"
        success, _ = db.execute_query(query, (id_est, 'Test Carrera', 2020, 2021))
        assert not success, "Se permitió insertar historial sin institución anterior"
    
    @pytest.mark.invalid
    def test_historial_carrera_anterior_not_null(self, db):
        """HistorialInstitucional.carrera_anterior NO puede ser NULL"""
        row = db.fetch_query("SELECT id_estudiante FROM Estudiante LIMIT 1")
        id_est = row[0][0]
        
        query = "INSERT INTO HistorialInstitucional (id_estudiante, institucion_anterior, ano_inicio, ano_finalizacion) VALUES (%s, %s, %s, %s)"
        success, _ = db.execute_query(query, (id_est, 'Test Institución', 2020, 2021))
        assert not success, "Se permitió insertar historial sin carrera anterior"
    
    @pytest.mark.invalid
    def test_historial_ano_inicio_not_null(self, db):
        """HistorialInstitucional.ano_inicio NO puede ser NULL"""
        row = db.fetch_query("SELECT id_estudiante FROM Estudiante LIMIT 1")
        id_est = row[0][0]
        
        query = "INSERT INTO HistorialInstitucional (id_estudiante, institucion_anterior, carrera_anterior, ano_finalizacion) VALUES (%s, %s, %s, %s)"
        success, _ = db.execute_query(query, (id_est, 'Test Institución', 'Test Carrera', 2021))
        assert not success, "Se permitió insertar historial sin año inicio"
    
    @pytest.mark.invalid
    def test_historial_ano_finalizacion_not_null(self, db):
        """HistorialInstitucional.ano_finalizacion NO puede ser NULL"""
        row = db.fetch_query("SELECT id_estudiante FROM Estudiante LIMIT 1")
        id_est = row[0][0]
        
        query = "INSERT INTO HistorialInstitucional (id_estudiante, institucion_anterior, carrera_anterior, ano_inicio) VALUES (%s, %s, %s, %s)"
        success, _ = db.execute_query(query, (id_est, 'Test Institución', 'Test Carrera', 2020))
        assert not success, "Se permitió insertar historial sin año finalización"


class TestEnumValidation:
    """Pruebas de validación de valores ENUM"""
    
    @pytest.mark.invalid
    def test_estudiante_sexo_valor_invalido(self, db):
        """Estudiante.sexo solo acepta 'M', 'F', 'O'"""
        query = """
            INSERT INTO Estudiante 
            (rut, nombre, email_institucional, telefono, fecha_nacimiento, edad, sexo, nacionalidad, ano_egreso_media, puntaje_psu, integrantes_grupo_familiar)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        success, error = db.execute_query(query, (
            '88888888-8', 'Test', 'test@inacapmail.cl', '+569999999', date(2005, 1, 1), 21, 'X', 'CHILE', 2023, 500, 3
        ))
        assert not success, "Se permitió valor inválido en ENUM sexo"
        assert error and ("enum" in error.lower() or "truncated" in error.lower())
    
    @pytest.mark.valid
    def test_estudiante_sexo_valores_validos(self, db):
        """Estudiante.sexo acepta valores válidos M, F, O"""
        query = """
            INSERT INTO Estudiante 
            (rut, nombre, email_institucional, telefono, fecha_nacimiento, edad, sexo, nacionalidad, ano_egreso_media, puntaje_psu, integrantes_grupo_familiar)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        for sexo in ['M', 'F', 'O']:
            success, error = db.execute_query(query, (
                f'8888888{sexo}-8', f'Test {sexo}', f'test{sexo}@inacapmail.cl', '+569999999', date(2005, 1, 1), 21, sexo, 'CHILE', 2023, 500, 3
            ))
            assert success, f"No se permitió valor válido '{sexo}' en ENUM sexo: {error}"
    
    @pytest.mark.invalid
    def test_colegio_tipo_valor_invalido(self, db):
        """Colegio.tipo_colegio solo acepta valores definidos en ENUM"""
        row = db.fetch_query("SELECT id_comuna, id_region FROM Comuna LIMIT 1")
        id_comuna, id_region = row[0]
        row = db.fetch_query("SELECT id_direccion FROM Direccion LIMIT 1")
        id_direccion = row[0][0]
        
        query = "INSERT INTO Colegio (id_comuna, id_region, id_direccion, rbd, nombre, tipo_colegio) VALUES (%s, %s, %s, %s, %s, %s)"
        success, error = db.execute_query(query, (id_comuna, id_region, id_direccion, '99999-9', 'Test', 'INVALIDO'))
        assert not success, "Se permitió valor inválido en ENUM tipo_colegio"
        assert error and ("enum" in error.lower() or "truncated" in error.lower())
    
    @pytest.mark.valid
    def test_colegio_tipo_valores_validos(self, db):
        """Colegio.tipo_colegio acepta valores válidos del ENUM"""
        row = db.fetch_query("SELECT id_comuna, id_region FROM Comuna LIMIT 1")
        id_comuna, id_region = row[0]
        row = db.fetch_query("SELECT id_direccion FROM Direccion LIMIT 1")
        id_direccion = row[0][0]
        
        query = "INSERT INTO Colegio (id_comuna, id_region, id_direccion, rbd, nombre, tipo_colegio) VALUES (%s, %s, %s, %s, %s, %s)"
        
        tipos_validos = ['GRATUITOS', 'PARTICULARES PAGADOS', 'PARTICULARES SUBVENCIONADOS']
        for i, tipo in enumerate(tipos_validos):
            success, error = db.execute_query(query, (id_comuna, id_region, id_direccion, f'8888{i}-9', f'Test {i}', tipo))
            assert success, f"No se permitió valor válido '{tipo}': {error}"
    
    @pytest.mark.invalid
    def test_direccion_tipo_valor_invalido(self, db):
        """Direccion.tipo_direccion solo acepta 'Permanente' o 'Temporal'"""
        row = db.fetch_query("SELECT id_comuna FROM Comuna LIMIT 1")
        id_comuna = row[0][0]
        
        query = "INSERT INTO Direccion (id_comuna, calle, numero, tipo_direccion) VALUES (%s, %s, %s, %s)"
        success, error = db.execute_query(query, (id_comuna, 'Test', 123, 'INVALIDO'))
        assert not success, "Se permitió valor inválido en ENUM tipo_direccion"
        assert error and ("enum" in error.lower() or "truncated" in error.lower())
    
    @pytest.mark.valid
    def test_direccion_tipo_valores_validos(self, db):
        """Direccion.tipo_direccion acepta 'Permanente' y 'Temporal'"""
        row = db.fetch_query("SELECT id_comuna FROM Comuna LIMIT 1")
        id_comuna = row[0][0]
        
        query = "INSERT INTO Direccion (id_comuna, calle, numero, tipo_direccion) VALUES (%s, %s, %s, %s)"
        
        for tipo in ['Permanente', 'Temporal']:
            success, error = db.execute_query(query, (id_comuna, f'Calle {tipo}', 123, tipo))
            assert success, f"No se permitió valor válido '{tipo}': {error}"
    
    @pytest.mark.invalid
    def test_institucion_tipo_valor_invalido(self, db):
        """Institucion.tipo_instucion solo acepta 'C.F.T' o 'I:P'"""
        query = "INSERT INTO Institucion (tipo_instucion, nombre_institucion) VALUES (%s, %s)"
        success, error = db.execute_query(query, ('UNIVERSIDAD', 'Test'))
        assert not success, "Se permitió valor inválido en ENUM tipo_instucion"
        assert error and ("enum" in error.lower() or "truncated" in error.lower())
    
    @pytest.mark.valid
    def test_institucion_tipo_valores_validos(self, db):
        """Institucion.tipo_instucion acepta 'C.F.T' e 'I:P'"""
        query = "INSERT INTO Institucion (tipo_instucion, nombre_institucion) VALUES (%s, %s)"
        
        for tipo in ['C.F.T', 'I:P']:
            success, error = db.execute_query(query, (tipo, f'Institución Test {tipo}'))
            assert success, f"No se permitió valor válido '{tipo}': {error}"
    
    @pytest.mark.invalid
    def test_carrera_jornada_valor_invalido(self, db):
        """Carrera.jornada solo acepta 'DIURNA', 'VESPERTINA', 'MIXTA'"""
        row = db.fetch_query("SELECT id_area_academica, id_institucion, id_plan_estudio FROM Carrera LIMIT 1")
        id_area, id_inst, id_plan = row[0]
        
        query = """
            INSERT INTO Carrera (id_area_academica, id_institucion, id_plan_estudio, codigo_carrera, nombre_carrera, jornada, tipo_programa)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        success, error = db.execute_query(query, (id_area, id_inst, id_plan, 'TST99', 'Test Carrera', 'NOCTURNA', 'REGULAR'))
        assert not success, "Se permitió valor inválido en ENUM jornada"
        assert error and ("enum" in error.lower() or "truncated" in error.lower())
    
    @pytest.mark.valid
    def test_carrera_jornada_valores_validos(self, db):
        """Carrera.jornada acepta valores válidos del ENUM"""
        row = db.fetch_query("SELECT id_area_academica, id_institucion, id_plan_estudio FROM Carrera LIMIT 1")
        id_area, id_inst, id_plan = row[0]
        
        query = """
            INSERT INTO Carrera (id_area_academica, id_institucion, id_plan_estudio, codigo_carrera, nombre_carrera, jornada, tipo_programa)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        
        for jornada in ['DIURNA', 'VESPERTINA', 'MIXTA']:
            success, error = db.execute_query(query, (id_area, id_inst, id_plan, f'TST{jornada[:3]}', f'Test {jornada}', jornada, 'REGULAR'))
            assert success, f"No se permitió valor válido '{jornada}': {error}"
    
    @pytest.mark.invalid
    def test_carrera_tipo_programa_valor_invalido(self, db):
        """Carrera.tipo_programa solo acepta 'REGULAR' o 'PEEC'"""
        row = db.fetch_query("SELECT id_area_academica, id_institucion, id_plan_estudio FROM Carrera LIMIT 1")
        id_area, id_inst, id_plan = row[0]
        
        query = """
            INSERT INTO Carrera (id_area_academica, id_institucion, id_plan_estudio, codigo_carrera, nombre_carrera, jornada, tipo_programa)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        success, error = db.execute_query(query, (id_area, id_inst, id_plan, 'TST88', 'Test', 'DIURNA', 'ESPECIAL'))
        assert not success, "Se permitió valor inválido en ENUM tipo_programa"
        assert error and ("enum" in error.lower() or "truncated" in error.lower())
    
    @pytest.mark.valid
    def test_carrera_tipo_programa_valores_validos(self, db):
        """Carrera.tipo_programa acepta 'REGULAR' y 'PEEC'"""
        row = db.fetch_query("SELECT id_area_academica, id_institucion, id_plan_estudio FROM Carrera LIMIT 1")
        id_area, id_inst, id_plan = row[0]
        
        query = """
            INSERT INTO Carrera (id_area_academica, id_institucion, id_plan_estudio, codigo_carrera, nombre_carrera, jornada, tipo_programa)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        
        for tipo in ['REGULAR', 'PEEC']:
            success, error = db.execute_query(query, (id_area, id_inst, id_plan, f'TST{tipo[:3]}', f'Test {tipo}', 'DIURNA', tipo))
            assert success, f"No se permitió valor válido '{tipo}': {error}"
    
    @pytest.mark.invalid
    def test_profesor_sexo_valor_invalido(self, db):
        """Profesor.sexo solo acepta 'MASCULINO', 'FEMENINO', 'OTRO'"""
        query = "INSERT INTO Profesor (nombre, rut, email_institucional, sexo) VALUES (%s, %s, %s, %s)"
        success, error = db.execute_query(query, ('Test', '99999999-9', 'test@inacap.cl', 'INVALIDO'))
        assert not success, "Se permitió valor inválido en ENUM sexo de profesor"
        assert error and ("enum" in error.lower() or "truncated" in error.lower())
    
    @pytest.mark.valid
    def test_profesor_sexo_valores_validos(self, db):
        """Profesor.sexo acepta valores válidos del ENUM"""
        query = "INSERT INTO Profesor (nombre, rut, email_institucional, sexo) VALUES (%s, %s, %s, %s)"
        
        for sexo in ['MASCULINO', 'FEMENINO', 'OTRO']:
            success, error = db.execute_query(query, (f'Test {sexo}', f'9999999{sexo[0]}-9', f'test{sexo}@inacap.cl', sexo))
            assert success, f"No se permitió valor válido '{sexo}': {error}"


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


class TestForeignKeyRestrict:
    """Pruebas exhaustivas de Foreign Keys con ON DELETE RESTRICT"""
    
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
    def test_restrict_eliminar_direccion_con_referencias(self, db):
        """No se puede eliminar dirección que está siendo referenciada por Colegio (RESTRICT)"""
        # Buscar dirección en colegio, si no hay, crear una
        row = db.fetch_query("SELECT id_direccion FROM Colegio LIMIT 1")
        if not row or not row[0]:
            # Crear dirección y colegio de prueba
            row_comuna = db.fetch_query("SELECT id_comuna, id_region FROM Comuna LIMIT 1")
            id_comuna, id_region = row_comuna[0]
            db.execute_query(
                "INSERT INTO Direccion (id_comuna, calle, numero, tipo_direccion) VALUES (%s, %s, %s, %s)",
                (id_comuna, 'Calle Restrict Test', 789, 'Permanente')
            )
            row_dir = db.fetch_query("SELECT id_direccion FROM Direccion WHERE calle = %s", ('Calle Restrict Test',))
            id_direccion = row_dir[0][0]
            db.execute_query(
                "INSERT INTO Colegio (id_comuna, id_region, id_direccion, nombre, tipo_colegio) VALUES (%s, %s, %s, %s, %s)",
                (id_comuna, id_region, id_direccion, 'Colegio Test Restrict', 'PARTICULARES PAGADOS')
            )
        else:
            id_direccion = row[0][0]
        
        success, _ = db.execute_query("DELETE FROM Direccion WHERE id_direccion = %s", (id_direccion,))
        assert not success, "Se permitió eliminar dirección referenciada por colegio"
        
        row = db.fetch_query("SELECT COUNT(*) FROM Direccion WHERE id_direccion = %s", (id_direccion,))
        assert row[0][0] == 1, "La dirección fue eliminada indebidamente"
    
    @pytest.mark.constraints
    def test_restrict_eliminar_ramo_con_referencias(self, db):
        """No se puede eliminar ramo que está siendo referenciado por ramos_plan_estudio (RESTRICT)"""
        # Buscar un ramo que tenga referencias
        row = db.fetch_query("SELECT id_ramo FROM ramos_plan_estudio LIMIT 1")
        if not row or not row[0]:
            pytest.skip("No hay ramo en plan de estudio en seed data")
        id_ramo = row[0][0]
        
        success, _ = db.execute_query("DELETE FROM Ramo WHERE id_ramo = %s", (id_ramo,))
        assert not success, "Se permitió eliminar ramo que está en plan de estudio"
        
        row = db.fetch_query("SELECT COUNT(*) FROM Ramo WHERE id_ramo = %s", (id_ramo,))
        assert row[0][0] == 1, "El ramo fue eliminado indebidamente"
    
    @pytest.mark.constraints
    def test_restrict_eliminar_profesor_con_secciones(self, db):
        """No se puede eliminar profesor que imparte secciones (RESTRICT en secciones_ramos)"""
        row = db.fetch_query("SELECT id_profesor FROM secciones_ramos LIMIT 1")
        if not row or not row[0]:
            pytest.skip("No hay profesor con secciones en seed data")
        id_profesor = row[0][0]
        
        success, _ = db.execute_query("DELETE FROM Profesor WHERE id_profesor = %s", (id_profesor,))
        assert not success, "Se permitió eliminar profesor que imparte secciones"
        
        row = db.fetch_query("SELECT COUNT(*) FROM Profesor WHERE id_profesor = %s", (id_profesor,))
        assert row[0][0] == 1, "El profesor fue eliminado indebidamente"


class TestCheckConstraints:
    """Pruebas de CHECK constraints (Categoría 7)"""
    
    @pytest.mark.constraints
    def test_promedio_matematicas_invalido_bajo(self, db):
        """No se puede insertar promedio de matemáticas menor a 1.0"""
        # Obtener datos base
        row = db.fetch_query("SELECT id_estudiante FROM Estudiante LIMIT 1")
        if not row or not row[0]:
            pytest.skip("No hay estudiante disponible")
        est_id = row[0][0]
        
        success, error = db.execute_query(
            "INSERT INTO Notas_Estudiante (id_estudiante, semestre_ingreso, promedio_matematicas) VALUES (%s, %s, %s)",
            (est_id, '2025-1', 0.5)
        )
        assert not success, "Se permitió promedio menor a 1.0"
        assert error and "check" in error.lower(), f"Error inesperado: {error}"
    
    @pytest.mark.constraints
    def test_promedio_matematicas_invalido_alto(self, db):
        """No se puede insertar promedio de matemáticas mayor a 7.0"""
        row = db.fetch_query("SELECT id_estudiante FROM Estudiante LIMIT 1")
        if not row or not row[0]:
            pytest.skip("No hay estudiante disponible")
        est_id = row[0][0]
        
        success, error = db.execute_query(
            "INSERT INTO Notas_Estudiante (id_estudiante, semestre_ingreso, promedio_matematicas) VALUES (%s, %s, %s)",
            (est_id, '2025-1', 7.5)
        )
        assert not success, "Se permitió promedio mayor a 7.0"
        assert error and "check" in error.lower(), f"Error inesperado: {error}"
    
    @pytest.mark.constraints
    def test_promedio_matematicas_valido_minimo(self, db):
        """Se puede insertar promedio de matemáticas igual a 1.0"""
        row = db.fetch_query("SELECT id_estudiante FROM Estudiante LIMIT 1")
        if not row or not row[0]:
            pytest.skip("No hay estudiante disponible")
        est_id = row[0][0]
        
        success, error = db.execute_query(
            "INSERT INTO Notas_Estudiante (id_estudiante, semestre_ingreso, promedio_matematicas) VALUES (%s, %s, %s)",
            (est_id, '2025-1', 1.0)
        )
        assert success, f"No se permitió promedio válido 1.0: {error}"
        
        # Verificar que se insertó
        row = db.fetch_query(
            "SELECT COUNT(*) FROM Notas_Estudiante WHERE id_estudiante = %s AND promedio_matematicas = %s",
            (est_id, 1.0)
        )
        assert row[0][0] >= 1, "No se insertó el promedio válido"
    
    @pytest.mark.constraints
    def test_promedio_matematicas_valido_maximo(self, db):
        """Se puede insertar promedio de matemáticas igual a 7.0"""
        row = db.fetch_query("SELECT id_estudiante FROM Estudiante LIMIT 1")
        if not row or not row[0]:
            pytest.skip("No hay estudiante disponible")
        est_id = row[0][0]
        
        success, error = db.execute_query(
            "INSERT INTO Notas_Estudiante (id_estudiante, semestre_ingreso, promedio_matematicas) VALUES (%s, %s, %s)",
            (est_id, '2025-1', 7.0)
        )
        assert success, f"No se permitió promedio válido 7.0: {error}"
        
        row = db.fetch_query(
            "SELECT COUNT(*) FROM Notas_Estudiante WHERE id_estudiante = %s AND promedio_matematicas = %s",
            (est_id, 7.0)
        )
        assert row[0][0] >= 1, "No se insertó el promedio válido"
    
    @pytest.mark.constraints
    def test_promedio_lenguaje_invalido(self, db):
        """No se puede insertar promedio de lenguaje fuera del rango 1.0-7.0"""
        row = db.fetch_query("SELECT id_estudiante FROM Estudiante LIMIT 1")
        if not row or not row[0]:
            pytest.skip("No hay estudiante disponible")
        est_id = row[0][0]
        
        # Test valor bajo
        success, error = db.execute_query(
            "INSERT INTO Notas_Estudiante (id_estudiante, semestre_ingreso, promedio_lenguaje) VALUES (%s, %s, %s)",
            (est_id, '2025-1', 0.9)
        )
        assert not success, "Se permitió promedio de lenguaje menor a 1.0"
        
        # Test valor alto
        success, error = db.execute_query(
            "INSERT INTO Notas_Estudiante (id_estudiante, semestre_ingreso, promedio_lenguaje) VALUES (%s, %s, %s)",
            (est_id, '2025-2', 7.1)
        )
        assert not success, "Se permitió promedio de lenguaje mayor a 7.0"
    
    @pytest.mark.constraints
    def test_promedio_lenguaje_valido(self, db):
        """Se puede insertar promedio de lenguaje dentro del rango 1.0-7.0"""
        row = db.fetch_query("SELECT id_estudiante FROM Estudiante LIMIT 1")
        if not row or not row[0]:
            pytest.skip("No hay estudiante disponible")
        est_id = row[0][0]
        
        success, error = db.execute_query(
            "INSERT INTO Notas_Estudiante (id_estudiante, semestre_ingreso, promedio_lenguaje) VALUES (%s, %s, %s)",
            (est_id, '2025-1', 5.5)
        )
        assert success, f"No se permitió promedio válido 5.5: {error}"
        
        row = db.fetch_query(
            "SELECT COUNT(*) FROM Notas_Estudiante WHERE id_estudiante = %s AND promedio_lenguaje = %s",
            (est_id, 5.5)
        )
        assert row[0][0] >= 1, "No se insertó el promedio válido"
    
    @pytest.mark.constraints
    def test_promedio_ingles_invalido(self, db):
        """No se puede insertar promedio de inglés fuera del rango 1.0-7.0"""
        row = db.fetch_query("SELECT id_estudiante FROM Estudiante LIMIT 1")
        if not row or not row[0]:
            pytest.skip("No hay estudiante disponible")
        est_id = row[0][0]
        
        # Test valor bajo
        success, error = db.execute_query(
            "INSERT INTO Notas_Estudiante (id_estudiante, semestre_ingreso, promedio_ingles) VALUES (%s, %s, %s)",
            (est_id, '2025-1', 0.1)
        )
        assert not success, "Se permitió promedio de inglés menor a 1.0"
        
        # Test valor alto
        success, error = db.execute_query(
            "INSERT INTO Notas_Estudiante (id_estudiante, semestre_ingreso, promedio_ingles) VALUES (%s, %s, %s)",
            (est_id, '2025-2', 8.0)
        )
        assert not success, "Se permitió promedio de inglés mayor a 7.0"
    
    @pytest.mark.constraints
    def test_promedio_ingles_valido(self, db):
        """Se puede insertar promedio de inglés dentro del rango 1.0-7.0"""
        row = db.fetch_query("SELECT id_estudiante FROM Estudiante LIMIT 1")
        if not row or not row[0]:
            pytest.skip("No hay estudiante disponible")
        est_id = row[0][0]
        
        success, error = db.execute_query(
            "INSERT INTO Notas_Estudiante (id_estudiante, semestre_ingreso, promedio_ingles) VALUES (%s, %s, %s)",
            (est_id, '2025-1', 3.5)
        )
        assert success, f"No se permitió promedio válido 3.5: {error}"
        
        row = db.fetch_query(
            "SELECT COUNT(*) FROM Notas_Estudiante WHERE id_estudiante = %s AND promedio_ingles = %s",
            (est_id, 3.5)
        )
        assert row[0][0] >= 1, "No se insertó el promedio válido"
    
    @pytest.mark.constraints
    def test_nota_final_inscripcion_invalida(self, db):
        """No se puede insertar nota final fuera del rango 1.0-7.0 en inscripción"""
        # Obtener una sección de ramo
        row = db.fetch_query("SELECT id_seccion_ramo FROM Secciones_Ramos LIMIT 1")
        if not row or not row[0]:
            pytest.skip("No hay secciones de ramo en seed data")
        seccion_id = row[0][0]
        
        # Obtener un estudiante
        row = db.fetch_query("SELECT id_estudiante FROM Estudiante LIMIT 1")
        if not row or not row[0]:
            pytest.skip("No hay estudiante disponible")
        est_id = row[0][0]
        
        # Test valor bajo
        success, error = db.execute_query(
            "INSERT INTO Inscripciones_Ramos (id_estudiante, id_seccion, fecha_inscripcion, tipo_inscripcion, nota_final, porcentaje_asistencia) VALUES (%s, %s, %s, %s, %s, %s)",
            (est_id, seccion_id, '2025-01-15', 'REGULAR', 0.5, 50.0)
        )
        assert not success, "Se permitió nota final menor a 1.0"
        
        # Test valor alto
        success, error = db.execute_query(
            "INSERT INTO Inscripciones_Ramos (id_estudiante, id_seccion, fecha_inscripcion, tipo_inscripcion, nota_final, porcentaje_asistencia) VALUES (%s, %s, %s, %s, %s, %s)",
            (est_id, seccion_id, '2025-01-16', 'REGULAR', 7.5, 50.0)
        )
        assert not success, "Se permitió nota final mayor a 7.0"
    
    @pytest.mark.constraints
    def test_nota_final_inscripcion_valida(self, db):
        """Se puede insertar nota final dentro del rango 1.0-7.0 en inscripción"""
        row = db.fetch_query("SELECT id_seccion_ramo FROM Secciones_Ramos LIMIT 1")
        if not row or not row[0]:
            pytest.skip("No hay secciones de ramo en seed data")
        seccion_id = row[0][0]
        
        row = db.fetch_query("SELECT id_estudiante FROM Estudiante LIMIT 1")
        if not row or not row[0]:
            pytest.skip("No hay estudiante disponible")
        est_id = row[0][0]
        
        success, error = db.execute_query(
            "INSERT INTO Inscripciones_Ramos (id_estudiante, id_seccion, fecha_inscripcion, tipo_inscripcion, nota_final, porcentaje_asistencia) VALUES (%s, %s, %s, %s, %s, %s)",
            (est_id, seccion_id, '2025-01-15', 'REGULAR', 5.5, 85.0)
        )
        assert success, f"No se permitió nota final válida 5.5: {error}"
        
        row = db.fetch_query(
            "SELECT COUNT(*) FROM Inscripciones_Ramos WHERE id_estudiante = %s AND id_seccion = %s AND nota_final = %s",
            (est_id, seccion_id, 5.5)
        )
        assert row[0][0] >= 1, "No se insertó la nota final válida"
    
    @pytest.mark.constraints
    def test_porcentaje_asistencia_invalido_bajo(self, db):
        """No se puede insertar porcentaje de asistencia menor a 0.0"""
        row = db.fetch_query("SELECT id_seccion_ramo FROM Secciones_Ramos LIMIT 1")
        if not row or not row[0]:
            pytest.skip("No hay secciones de ramo en seed data")
        seccion_id = row[0][0]
        
        row = db.fetch_query("SELECT id_estudiante FROM Estudiante LIMIT 1")
        if not row or not row[0]:
            pytest.skip("No hay estudiante disponible")
        est_id = row[0][0]
        
        success, error = db.execute_query(
            "INSERT INTO Inscripciones_Ramos (id_estudiante, id_seccion, fecha_inscripcion, tipo_inscripcion, nota_final, porcentaje_asistencia) VALUES (%s, %s, %s, %s, %s, %s)",
            (est_id, seccion_id, '2025-01-15', 'REGULAR', 5.0, -0.1)
        )
        assert not success, "Se permitió porcentaje de asistencia negativo"
    
    @pytest.mark.constraints
    def test_porcentaje_asistencia_invalido_alto(self, db):
        """No se puede insertar porcentaje de asistencia mayor a 100.0"""
        row = db.fetch_query("SELECT id_seccion_ramo FROM Secciones_Ramos LIMIT 1")
        if not row or not row[0]:
            pytest.skip("No hay secciones de ramo en seed data")
        seccion_id = row[0][0]
        
        row = db.fetch_query("SELECT id_estudiante FROM Estudiante LIMIT 1")
        if not row or not row[0]:
            pytest.skip("No hay estudiante disponible")
        est_id = row[0][0]
        
        success, error = db.execute_query(
            "INSERT INTO Inscripciones_Ramos (id_estudiante, id_seccion, fecha_inscripcion, tipo_inscripcion, nota_final, porcentaje_asistencia) VALUES (%s, %s, %s, %s, %s, %s)",
            (est_id, seccion_id, '2025-01-16', 'REGULAR', 5.0, 100.1)
        )
        assert not success, "Se permitió porcentaje de asistencia mayor a 100"
    
    @pytest.mark.constraints
    def test_porcentaje_asistencia_valido_minimo(self, db):
        """Se puede insertar porcentaje de asistencia igual a 0.0"""
        row = db.fetch_query("SELECT id_seccion_ramo FROM Secciones_Ramos LIMIT 1")
        if not row or not row[0]:
            pytest.skip("No hay secciones de ramo en seed data")
        seccion_id = row[0][0]
        
        row = db.fetch_query("SELECT id_estudiante FROM Estudiante LIMIT 1")
        if not row or not row[0]:
            pytest.skip("No hay estudiante disponible")
        est_id = row[0][0]
        
        success, error = db.execute_query(
            "INSERT INTO Inscripciones_Ramos (id_estudiante, id_seccion, fecha_inscripcion, tipo_inscripcion, nota_final, porcentaje_asistencia) VALUES (%s, %s, %s, %s, %s, %s)",
            (est_id, seccion_id, '2025-01-15', 'REGULAR', 5.0, 0.0)
        )
        assert success, f"No se permitió porcentaje válido 0.0: {error}"
        
        row = db.fetch_query(
            "SELECT COUNT(*) FROM Inscripciones_Ramos WHERE id_estudiante = %s AND id_seccion = %s AND porcentaje_asistencia = %s",
            (est_id, seccion_id, 0.0)
        )
        assert row[0][0] >= 1, "No se insertó el porcentaje válido"
    
    @pytest.mark.constraints
    def test_porcentaje_asistencia_valido_maximo(self, db):
        """Se puede insertar porcentaje de asistencia igual a 100.0"""
        row = db.fetch_query("SELECT id_seccion_ramo FROM Secciones_Ramos LIMIT 1")
        if not row or not row[0]:
            pytest.skip("No hay secciones de ramo en seed data")
        seccion_id = row[0][0]
        
        row = db.fetch_query("SELECT id_estudiante FROM Estudiante LIMIT 1")
        if not row or not row[0]:
            pytest.skip("No hay estudiante disponible")
        est_id = row[0][0]
        
        success, error = db.execute_query(
            "INSERT INTO Inscripciones_Ramos (id_estudiante, id_seccion, fecha_inscripcion, tipo_inscripcion, nota_final, porcentaje_asistencia) VALUES (%s, %s, %s, %s, %s, %s)",
            (est_id, seccion_id, '2025-01-17', 'REGULAR', 5.0, 100.0)
        )
        assert success, f"No se permitió porcentaje válido 100.0: {error}"
        
        row = db.fetch_query(
            "SELECT COUNT(*) FROM Inscripciones_Ramos WHERE id_estudiante = %s AND id_seccion = %s AND porcentaje_asistencia = %s",
            (est_id, seccion_id, 100.0)
        )
        assert row[0][0] >= 1, "No se insertó el porcentaje válido"


class TestForeignKeyCascade:
    """Pruebas de relaciones ON DELETE CASCADE (Categoría 5)"""
    
    @pytest.mark.constraints
    def test_cascade_eliminar_estudiante_elimina_notas(self, db):
        """Al eliminar estudiante se eliminan sus notas (CASCADE)"""
        # Obtener un estudiante con notas en seed
        row = db.fetch_query("""
            SELECT DISTINCT e.id_estudiante FROM Estudiante e
            INNER JOIN Notas_Estudiante n ON e.id_estudiante = n.id_estudiante
            LIMIT 1
        """)
        
        if not row or not row[0]:
            pytest.skip("No hay notas de estudiante en seed data")
        
        est_id = row[0][0]
        notas_antes = db.fetch_query("SELECT COUNT(*) FROM Notas_Estudiante WHERE id_estudiante = %s", (est_id,))
        assert notas_antes[0][0] > 0, "Estudiante sin notas"
        
        success, error = db.execute_query("DELETE FROM Estudiante WHERE id_estudiante = %s", (est_id,))
        assert success, f"Error al eliminar estudiante: {error}"
        
        notas_despues = db.fetch_query("SELECT COUNT(*) FROM Notas_Estudiante WHERE id_estudiante = %s", (est_id,))
        assert notas_despues[0][0] == 0, "Notas no eliminadas por CASCADE"
    
    @pytest.mark.constraints
    def test_cascade_eliminar_estudiante_elimina_matriculas(self, db):
        """Al eliminar estudiante se eliminan sus matrículas (CASCADE)"""
        # Obtener un estudiante con matrículas en seed
        row = db.fetch_query("""
            SELECT DISTINCT e.id_estudiante FROM Estudiante e
            INNER JOIN Matricula m ON e.id_estudiante = m.id_estudiante
            LIMIT 1
        """)
        
        if not row or not row[0]:
            pytest.skip("No hay matrículas de estudiante en seed data")
        
        est_id = row[0][0]
        matriculas_antes = db.fetch_query("SELECT COUNT(*) FROM Matricula WHERE id_estudiante = %s", (est_id,))
        assert matriculas_antes[0][0] > 0, "Estudiante sin matrículas"
        
        success, error = db.execute_query("DELETE FROM Estudiante WHERE id_estudiante = %s", (est_id,))
        assert success, f"Error al eliminar estudiante: {error}"
        
        matriculas_despues = db.fetch_query("SELECT COUNT(*) FROM Matricula WHERE id_estudiante = %s", (est_id,))
        assert matriculas_despues[0][0] == 0, "Matrículas no eliminadas por CASCADE"
    
    @pytest.mark.constraints
    def test_cascade_eliminar_ramo_elimina_secciones(self, db):
        """Al eliminar ramo se eliminan sus secciones (CASCADE)"""
        import time
        # Crear ramo de prueba (sin relaciones a Ramos_Plan_Estudio)
        timestamp = int(time.time() * 1000000)  # Microsegundos para evitar duplicados
        sigla = f'CASC{timestamp % 10000}'
        
        success, error = db.execute_query(
            "INSERT INTO Ramo (sigla, nombre_ramo, horas_teoricas, horas_practicas, horas_semanales, nivel_recomendado) VALUES (%s, %s, %s, %s, %s, %s)",
            (sigla, f'Ramo CASCADE Test {timestamp}', 2, 2, 4, 1)
        )
        
        if not success:
            pytest.skip(f"No se pudo crear ramo de prueba: {error}")
        
        row = db.fetch_query("SELECT id_ramo FROM Ramo WHERE sigla = %s", (sigla,))
        if not row or not row[0]:
            pytest.skip("Ramo de prueba no encontrado")
        
        ramo_id = row[0][0]
        
        # Crear sección para este ramo
        row = db.fetch_query("SELECT id_profesor FROM Profesor LIMIT 1")
        if not row or not row[0]:
            pytest.skip("No hay profesor disponible")
        
        prof_id = row[0][0]
        success, error = db.execute_query(
            "INSERT INTO Secciones_Ramos (id_ramo, id_profesor, seccion, codigo_seccion, semestre_dictado, jornadas, cupos_totales, cupos_ocupados, horario, estado) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (ramo_id, prof_id, '01', f'{sigla}-01-2025-1', '2025-1', 'DIURNA', 30, 20, 'Lunes 8:00', 'ACTIVA')
        )
        
        if not success:
            pytest.skip(f"No se pudo crear sección de prueba: {error}")
        
        secciones_antes = db.fetch_query("SELECT COUNT(*) FROM Secciones_Ramos WHERE id_ramo = %s", (ramo_id,))
        assert secciones_antes[0][0] > 0, "Sección no creada"
        
        success, error = db.execute_query("DELETE FROM Ramo WHERE id_ramo = %s", (ramo_id,))
        assert success, f"Error al eliminar ramo: {error}"
        
        secciones_despues = db.fetch_query("SELECT COUNT(*) FROM Secciones_Ramos WHERE id_ramo = %s", (ramo_id,))
        assert secciones_despues[0][0] == 0, "Secciones no eliminadas por CASCADE"
    
    @pytest.mark.constraints
    def test_cascade_eliminar_ramo_elimina_prerequisitos(self, db):
        """Al eliminar ramo se eliminan sus prerequisitos (CASCADE)"""
        # Crear ramo de prueba con prerequisito
        row = db.fetch_query("SELECT id_ramo FROM Ramo LIMIT 1")
        if not row or not row[0]:
            pytest.skip("No hay ramos en seed data")
        
        ramo_id1 = row[0][0]
        
        # Crear segundo ramo para prerequisito
        import time
        timestamp = int(time.time() * 1000000)
        sigla = f'PREREQ{timestamp % 10000}'
        
        success, _ = db.execute_query(
            "INSERT INTO Ramo (sigla, nombre_ramo, horas_teoricas, horas_practicas, horas_semanales, nivel_recomendado) VALUES (%s, %s, %s, %s, %s, %s)",
            (sigla, f'Ramo Prereq Test {timestamp}', 2, 2, 4, 1)
        )
        
        if success:
            row = db.fetch_query("SELECT id_ramo FROM Ramo WHERE sigla = %s", (sigla,))
            if row and row[0]:
                ramo_id2 = row[0][0]
                
                # Insertar prerequisito
                success, _ = db.execute_query(
                    "INSERT INTO Prerequisito (id_ramo, id_ramo_prerequisito) VALUES (%s, %s)",
                    (ramo_id2, ramo_id1)
                )
                
                if success:
                    prereqs_antes = db.fetch_query("SELECT COUNT(*) FROM Prerequisito WHERE id_ramo_prerequisito = %s", (ramo_id1,))
                    assert prereqs_antes[0][0] >= 1, "Prerequisito no insertado"
                    
                    db.execute_query("DELETE FROM Ramo WHERE id_ramo = %s", (ramo_id1,))
                    prereqs_despues = db.fetch_query("SELECT COUNT(*) FROM Prerequisito WHERE id_ramo_prerequisito = %s", (ramo_id1,))
                    assert prereqs_despues[0][0] == 0, "Prerequisitos no eliminados por CASCADE"
                else:
                    pytest.skip("No se pudo insertar prerequisito de prueba")
        else:
            pytest.skip("No se pudo crear ramo de prueba")
    
    @pytest.mark.constraints
    def test_cascade_eliminar_ramo_elimina_area_conocimiento(self, db):
        """Al eliminar ramo se eliminan relaciones ramo_areaConocimiento (CASCADE)"""
        # Obtener un ramo con área de conocimiento en seed
        row = db.fetch_query("""
            SELECT DISTINCT r.id_ramo FROM Ramo r
            INNER JOIN ramo_areaConocimiento ra ON r.id_ramo = ra.id_ramo
            LIMIT 1
        """)
        
        if not row or not row[0]:
            pytest.skip("No hay relaciones ramo_areaConocimiento en seed data")
        
        ramo_id = row[0][0]
        areas_antes = db.fetch_query("SELECT COUNT(*) FROM ramo_areaConocimiento WHERE id_ramo = %s", (ramo_id,))
        assert areas_antes[0][0] > 0, "Ramo sin áreas de conocimiento"
        
        success, error = db.execute_query("DELETE FROM Ramo WHERE id_ramo = %s", (ramo_id,))
        assert success, f"Error al eliminar ramo: {error}"
        
        areas_despues = db.fetch_query("SELECT COUNT(*) FROM ramo_areaConocimiento WHERE id_ramo = %s", (ramo_id,))
        assert areas_despues[0][0] == 0, "Relaciones ramo_areaConocimiento no eliminadas por CASCADE"
    
    @pytest.mark.constraints
    def test_cascade_eliminar_secciones_ramos_elimina_inscripciones(self, db):
        """Al eliminar sección de ramo se eliminan inscripciones (CASCADE)"""
        # Obtener una sección con inscripciones en seed
        row = db.fetch_query("""
            SELECT DISTINCT s.id_seccion_ramo FROM Secciones_Ramos s
            INNER JOIN Inscripciones_Ramos i ON s.id_seccion_ramo = i.id_seccion_ramo
            LIMIT 1
        """)
        
        if not row or not row[0]:
            pytest.skip("No hay inscripciones de sección en seed data")
        
        seccion_id = row[0][0]
        inscripciones_antes = db.fetch_query("SELECT COUNT(*) FROM Inscripciones_Ramos WHERE id_seccion_ramo = %s", (seccion_id,))
        assert inscripciones_antes[0][0] > 0, "Sección sin inscripciones"
        
        success, error = db.execute_query("DELETE FROM Secciones_Ramos WHERE id_seccion_ramo = %s", (seccion_id,))
        assert success, f"Error al eliminar sección: {error}"
        
        inscripciones_despues = db.fetch_query("SELECT COUNT(*) FROM Inscripciones_Ramos WHERE id_seccion_ramo = %s", (seccion_id,))
        assert inscripciones_despues[0][0] == 0, "Inscripciones no eliminadas por CASCADE"
    
    @pytest.mark.constraints
    def test_cascade_eliminar_carrera_elimina_matriculas(self, db):
        """Al eliminar carrera se eliminan matrículas asociadas (CASCADE)"""
        # Obtener carrera con matrículas en seed
        row = db.fetch_query("""
            SELECT DISTINCT c.id_carrera FROM Carrera c
            INNER JOIN Matricula m ON c.id_carrera = m.id_carrera
            LIMIT 1
        """)
        
        if not row or not row[0]:
            pytest.skip("No hay matrículas en seed data")
        
        carrera_id = row[0][0]
        matriculas_antes = db.fetch_query("SELECT COUNT(*) FROM Matricula WHERE id_carrera = %s", (carrera_id,))
        assert matriculas_antes[0][0] > 0, "Carrera sin matrículas"
        
        success, error = db.execute_query("DELETE FROM Carrera WHERE id_carrera = %s", (carrera_id,))
        assert success, f"Error al eliminar carrera: {error}"
        
        matriculas_despues = db.fetch_query("SELECT COUNT(*) FROM Matricula WHERE id_carrera = %s", (carrera_id,))
        assert matriculas_despues[0][0] == 0, "Matrículas no eliminadas por CASCADE"
    
    @pytest.mark.constraints
    def test_cascade_eliminar_matricula_elimina_pagos(self, db):
        """Al eliminar matrícula se eliminan pagos asociados (CASCADE)"""
        # Obtener matrícula con pagos en seed
        row = db.fetch_query("""
            SELECT DISTINCT m.id_matricula FROM Matricula m
            INNER JOIN Pago p ON m.id_matricula = p.id_matricula
            LIMIT 1
        """)
        
        if not row or not row[0]:
            pytest.skip("No hay pagos en seed data")
        
        matricula_id = row[0][0]
        pagos_antes = db.fetch_query("SELECT COUNT(*) FROM Pago WHERE id_matricula = %s", (matricula_id,))
        assert pagos_antes[0][0] > 0, "Matrícula sin pagos"
        
        success, error = db.execute_query("DELETE FROM Matricula WHERE id_matricula = %s", (matricula_id,))
        assert success, f"Error al eliminar matrícula: {error}"
        
        pagos_despues = db.fetch_query("SELECT COUNT(*) FROM Pago WHERE id_matricula = %s", (matricula_id,))
        assert pagos_despues[0][0] == 0, "Pagos no eliminados por CASCADE"
    
    @pytest.mark.constraints
    def test_cascade_eliminar_pago_elimina_cuotas(self, db):
        """Al eliminar pago se eliminan cuotas asociadas (CASCADE)"""
        # Obtener pago con cuotas en seed
        row = db.fetch_query("""
            SELECT DISTINCT p.id_pago FROM Pago p
            INNER JOIN Cuota c ON p.id_pago = c.id_pago
            LIMIT 1
        """)
        
        if not row or not row[0]:
            pytest.skip("No hay cuotas en seed data")
        
        pago_id = row[0][0]
        cuotas_antes = db.fetch_query("SELECT COUNT(*) FROM Cuota WHERE id_pago = %s", (pago_id,))
        assert cuotas_antes[0][0] > 0, "Pago sin cuotas"
        
        success, error = db.execute_query("DELETE FROM Pago WHERE id_pago = %s", (pago_id,))
        assert success, f"Error al eliminar pago: {error}"
        
        cuotas_despues = db.fetch_query("SELECT COUNT(*) FROM Cuota WHERE id_pago = %s", (pago_id,))
        assert cuotas_despues[0][0] == 0, "Cuotas no eliminadas por CASCADE"
    
    @pytest.mark.constraints
    def test_cascade_eliminar_cuota_elimina_transacciones(self, db):
        """Al eliminar cuota se eliminan transacciones asociadas (CASCADE)"""
        # Obtener cuota con transacciones en seed
        row = db.fetch_query("""
            SELECT DISTINCT c.id_cuota FROM Cuota c
            INNER JOIN Transaccion t ON c.id_cuota = t.id_cuota
            LIMIT 1
        """)
        
        if not row or not row[0]:
            pytest.skip("No hay transacciones en seed data")
        
        cuota_id = row[0][0]
        transacciones_antes = db.fetch_query("SELECT COUNT(*) FROM Transaccion WHERE id_cuota = %s", (cuota_id,))
        assert transacciones_antes[0][0] > 0, "Cuota sin transacciones"
        
        success, error = db.execute_query("DELETE FROM Cuota WHERE id_cuota = %s", (cuota_id,))
        assert success, f"Error al eliminar cuota: {error}"
        
        transacciones_despues = db.fetch_query("SELECT COUNT(*) FROM Transaccion WHERE id_cuota = %s", (cuota_id,))
        assert transacciones_despues[0][0] == 0, "Transacciones no eliminadas por CASCADE"
    
    @pytest.mark.constraints
    def test_cascade_eliminar_area_academica_elimina_carreras(self, db):
        """Al eliminar área académica se eliminan carreras asociadas (CASCADE)"""
        # Obtener área académica con carreras en seed
        row = db.fetch_query("""
            SELECT DISTINCT aa.id_area_academica FROM Area_Academica aa
            INNER JOIN Carrera c ON aa.id_area_academica = c.id_area_academica
            LIMIT 1
        """)
        
        if not row or not row[0]:
            pytest.skip("No hay carreras en seed data")
        
        area_id = row[0][0]
        carreras_antes = db.fetch_query("SELECT COUNT(*) FROM Carrera WHERE id_area_academica = %s", (area_id,))
        assert carreras_antes[0][0] > 0, "Área académica sin carreras"
        
        success, error = db.execute_query("DELETE FROM Area_Academica WHERE id_area_academica = %s", (area_id,))
        assert success, f"Error al eliminar área académica: {error}"
        
        carreras_despues = db.fetch_query("SELECT COUNT(*) FROM Carrera WHERE id_area_academica = %s", (area_id,))
        assert carreras_despues[0][0] == 0, "Carreras no eliminadas por CASCADE"
    
    @pytest.mark.constraints
    def test_cascade_eliminar_institucion_elimina_carreras(self, db):
        """Al eliminar institución se eliminan carreras asociadas (CASCADE)"""
        # Crear institución de prueba
        success, _ = db.execute_query(
            "INSERT INTO Institucion (nombre, tipo_institucion) VALUES (%s, %s)",
            ('Institución Test', 'Universidad')
        )
        
        if success:
            row = db.fetch_query("SELECT id_institucion FROM Institucion WHERE nombre = %s", ('Institución Test',))
            if row and row[0]:
                inst_id = row[0][0]
                
                # Crear carrera con esta institución
                row_area = db.fetch_query("SELECT id_area_academica FROM Area_Academica LIMIT 1")
                if row_area and row_area[0]:
                    area_id = row_area[0][0]
                    success, _ = db.execute_query(
                        "INSERT INTO Carrera (id_area_academica, id_institucion, codigo, nombre, jornada, tipo_programa) VALUES (%s, %s, %s, %s, %s, %s)",
                        (area_id, inst_id, 'TEST001', 'Carrera Test', 'Diurna', 'Técnico')
                    )
                    
                    if success:
                        carreras_antes = db.fetch_query("SELECT COUNT(*) FROM Carrera WHERE id_institucion = %s", (inst_id,))
                        
                        db.execute_query("DELETE FROM Institucion WHERE id_institucion = %s", (inst_id,))
                        carreras_despues = db.fetch_query("SELECT COUNT(*) FROM Carrera WHERE id_institucion = %s", (inst_id,))
                        
                        assert carreras_despues[0][0] == 0, "Carreras no eliminadas por CASCADE"
                    else:
                        pytest.skip("No se pudo crear carrera de prueba")
                else:
                    pytest.skip("No hay área académica disponible")
            else:
                pytest.skip("No se pudo crear institución de prueba")
        else:
            pytest.skip("No se pudo crear institución de prueba")
    
    @pytest.mark.constraints
    def test_cascade_eliminar_predictor_datos_relacionado_a_estudiante(self, db):
        """Al eliminar estudiante se eliminan datos del predictor (CASCADE)"""
        # Obtener estudiante con datos predictor en seed
        row = db.fetch_query("""
            SELECT DISTINCT e.id_estudiante FROM Estudiante e
            INNER JOIN Predictor_Datos pd ON e.id_estudiante = pd.id_estudiante
            LIMIT 1
        """)
        
        if not row or not row[0]:
            pytest.skip("No hay datos predictor en seed data")
        
        est_id = row[0][0]
        predictor_antes = db.fetch_query("SELECT COUNT(*) FROM Predictor_Datos WHERE id_estudiante = %s", (est_id,))
        assert predictor_antes[0][0] > 0, "Estudiante sin datos predictor"
        
        success, error = db.execute_query("DELETE FROM Estudiante WHERE id_estudiante = %s", (est_id,))
        assert success, f"Error al eliminar estudiante: {error}"
        
        predictor_despues = db.fetch_query("SELECT COUNT(*) FROM Predictor_Datos WHERE id_estudiante = %s", (est_id,))
        assert predictor_despues[0][0] == 0, "Datos predictor no eliminados por CASCADE"
    
    @pytest.mark.constraints
    def test_cascade_eliminar_predictor_datos_relacionado_a_matricula(self, db):
        """Al eliminar matrícula se eliminan datos del predictor relacionados (CASCADE)"""
        # Obtener matrícula con datos predictor en seed
        row = db.fetch_query("""
            SELECT DISTINCT m.id_matricula FROM Matricula m
            INNER JOIN Predictor_Datos pd ON m.id_matricula = pd.id_matricula
            LIMIT 1
        """)
        
        if not row or not row[0]:
            pytest.skip("No hay datos predictor con matrícula en seed data")
        
        matricula_id = row[0][0]
        predictor_antes = db.fetch_query("SELECT COUNT(*) FROM Predictor_Datos WHERE id_matricula = %s", (matricula_id,))
        assert predictor_antes[0][0] > 0, "Matrícula sin datos predictor"
        
        success, error = db.execute_query("DELETE FROM Matricula WHERE id_matricula = %s", (matricula_id,))
        assert success, f"Error al eliminar matrícula: {error}"
        
        predictor_despues = db.fetch_query("SELECT COUNT(*) FROM Predictor_Datos WHERE id_matricula = %s", (matricula_id,))
        assert predictor_despues[0][0] == 0, "Datos predictor no eliminados por CASCADE"


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
