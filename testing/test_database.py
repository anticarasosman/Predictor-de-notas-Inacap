"""
Test suite para la base de datos INACAP
Prueba inserciones válidas, inválidas y el funcionamiento de constraints (CASCADE y RESTRICT)
"""

import pytest
import mysql.connector
from mysql.connector import Error
from datetime import date
import os


class DatabaseManager:
    """Clase para manejar la conexión a la base de datos"""
    
    def __init__(self, host='localhost', user='root', password='', database='inacap_test'):
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


# ===== FIXTURES =====

@pytest.fixture(scope="function")
def db():
    """Fixture para inicializar y cerrar la conexión a BD"""
    db_manager = DatabaseManager()
    assert db_manager.connect(), "No se pudo conectar a la base de datos"
    db_manager.clear_tables()
    
    yield db_manager
    
    db_manager.disconnect()


# ===== TESTS DE INSERCIONES VÁLIDAS =====

class TestInsertarDatosValidos:
    """Pruebas de inserciones válidas en la base de datos"""
    
    def test_insertar_region(self, db):
        """Test: Insertar una región válida"""
        query = "INSERT INTO Region (codigo, nombre) VALUES (%s, %s)"
        success, error = db.execute_query(query, (11, 'Aysén del General Carlos Ibáñez del Campo'))
        
        assert success, f"Error al insertar región: {error}"
        
        # Verificar que se insertó
        result = db.fetch_query("SELECT * FROM Region WHERE codigo = 11")
        assert result is not None and len(result) > 0, "Región no encontrada después de insertar"
        assert result[0][2] == 'Aysén del General Carlos Ibáñez del Campo'
    
    def test_insertar_multiple_regiones(self, db):
        """Test: Insertar múltiples regiones"""
        regions = [
            (11, 'Aysén del General Carlos Ibáñez del Campo'),
            (5, 'Valparaíso'),
            (13, 'Metropolitana'),
        ]
        
        for codigo, nombre in regions:
            query = "INSERT INTO Region (codigo, nombre) VALUES (%s, %s)"
            success, error = db.execute_query(query, (codigo, nombre))
            assert success, f"Error al insertar región {nombre}: {error}"
        
        # Verificar que se insertaron las 3
        result = db.fetch_query("SELECT COUNT(*) FROM Region")
        assert result[0][0] == 3, "No se insertaron todas las regiones"
    
    def test_insertar_comuna(self, db):
        """Test: Insertar una comuna con región válida"""
        # Primero insertar región
        db.execute_query("INSERT INTO Region (codigo, nombre) VALUES (%s, %s)", 
                        (11, 'Aysén'))
        
        # Insertar comuna
        query = "INSERT INTO Comuna (id_region, codigo, nombre) VALUES (%s, %s, %s)"
        success, error = db.execute_query(query, (1, 1001, 'Coyhaique'))
        
        assert success, f"Error al insertar comuna: {error}"
    
    def test_insertar_colegio_completo(self, db):
        """Test: Insertar colegio con región y comuna"""
        # Insertar región
        db.execute_query("INSERT INTO Region (codigo, nombre) VALUES (%s, %s)", 
                        (11, 'Aysén'))
        
        # Insertar comuna
        db.execute_query("INSERT INTO Comuna (id_region, codigo, nombre) VALUES (%s, %s, %s)", 
                        (1, 1001, 'Coyhaique'))
        
        # Insertar colegio
        query = """INSERT INTO Colegio (id_comuna, id_region, rbd, nombre, tipo_colegio) 
                  VALUES (%s, %s, %s, %s, %s)"""
        success, error = db.execute_query(query, 
                                         (1, 1, '24206-3', 'Colegio Alborada', 'PARTICULARES PAGADOS'))
        
        assert success, f"Error al insertar colegio: {error}"
    
    def test_insertar_estudiante(self, db):
        """Test: Insertar un estudiante válido"""
        query = """INSERT INTO Estudiante 
                  (rut, nombre, email_institucional, telefono, fecha_nacimiento, edad, sexo, nacionalidad, ano_egreso_media, puntaje_psu, integrantes_grupo_familiar) 
                  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        
        success, error = db.execute_query(query, (
            '20587683-9',
            'Camila Manríquez Delgado',
            'camila.manriquez07@inacapmail.cl',
            '+569738539998',
            date(2004, 3, 15),
            21,
            'F',
            'CHILE',
            2022,
            550,
            4
        ))
        
        assert success, f"Error al insertar estudiante: {error}"
    
    def test_insertar_estudiante_direccion_bridge(self, db):
        """Test: Insertar relación estudiante-dirección"""
        # Insertar estudiante
        db.execute_query("""INSERT INTO Estudiante 
                          (rut, nombre, email_institucional, telefono, fecha_nacimiento, edad, sexo, nacionalidad, ano_egreso_media, puntaje_psu, integrantes_grupo_familiar) 
                          VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                        ('20587683-9', 'Camila', 'camila@inacapmail.cl', '+569738539998', 
                         date(2004, 3, 15), 21, 'F', 'CHILE', 2022, 550, 4))
        
        # Insertar región y comuna
        db.execute_query("INSERT INTO Region (codigo, nombre) VALUES (%s, %s)", (11, 'Aysén'))
        db.execute_query("INSERT INTO Comuna (id_region, codigo, nombre) VALUES (%s, %s, %s)", 
                        (1, 1001, 'Coyhaique'))
        
        # Insertar dirección
        db.execute_query("""INSERT INTO Direccion (id_comuna, calle, numero, tipo_direccion) 
                          VALUES (%s, %s, %s, %s)""",
                        (1, 'Calle Principal', 123, 'Permanente'))
        
        # Insertar en tabla bridge
        query = "INSERT INTO estudiante_direccion (estudiante_id) VALUES (%s)"
        success, error = db.execute_query(query, (1,))
        
        assert success, f"Error al insertar en tabla bridge: {error}"


# ===== TESTS DE INSERCIONES INVÁLIDAS =====

class TestInsertarDatosInvalidos:
    """Pruebas de inserciones inválidas (deben fallar)"""
    
    def test_region_codigo_duplicado(self, db):
        """Test: No permitir códigos de región duplicados"""
        # Insertar primera región
        db.execute_query("INSERT INTO Region (codigo, nombre) VALUES (%s, %s)", 
                        (11, 'Aysén'))
        
        # Intentar insertar con mismo código
        query = "INSERT INTO Region (codigo, nombre) VALUES (%s, %s)"
        success, error = db.execute_query(query, (11, 'Otra Región'))
        
        assert not success, "Se permitió insertar región con código duplicado"
        assert "UNIQUE" in error or "duplicate" in error.lower(), f"Error inesperado: {error}"
    
    def test_region_nombre_duplicado(self, db):
        """Test: No permitir nombres de región duplicados"""
        # Insertar primera región
        db.execute_query("INSERT INTO Region (codigo, nombre) VALUES (%s, %s)", 
                        (11, 'Aysén'))
        
        # Intentar insertar con mismo nombre
        query = "INSERT INTO Region (codigo, nombre) VALUES (%s, %s)"
        success, error = db.execute_query(query, (12, 'Aysén'))
        
        assert not success, "Se permitió insertar región con nombre duplicado"
    
    def test_comuna_sin_region(self, db):
        """Test: No permitir comuna sin región válida"""
        query = "INSERT INTO Comuna (id_region, codigo, nombre) VALUES (%s, %s, %s)"
        success, error = db.execute_query(query, (999, 1001, 'Coyhaique'))
        
        assert not success, "Se permitió insertar comuna sin región válida"
        assert "FOREIGN KEY" in error or "foreign key" in error.lower(), f"Error inesperado: {error}"
    
    def test_colegio_sin_comuna(self, db):
        """Test: No permitir colegio sin comuna válida"""
        # Insertar región
        db.execute_query("INSERT INTO Region (codigo, nombre) VALUES (%s, %s)", (11, 'Aysén'))
        
        # Intentar insertar colegio sin comuna válida
        query = """INSERT INTO Colegio (id_comuna, id_region, rbd, nombre, tipo_colegio) 
                  VALUES (%s, %s, %s, %s, %s)"""
        success, error = db.execute_query(query, 
                                         (999, 1, '24206-3', 'Colegio', 'PARTICULARES PAGADOS'))
        
        assert not success, "Se permitió insertar colegio sin comuna válida"
    
    def test_estudiante_email_duplicado(self, db):
        """Test: No permitir emails institucionales duplicados"""
        query = """INSERT INTO Estudiante 
                  (rut, nombre, email_institucional, telefono, fecha_nacimiento, edad, sexo, nacionalidad, ano_egreso_media, puntaje_psu, integrantes_grupo_familiar) 
                  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        
        # Insertar primer estudiante
        db.execute_query(query, (
            '20587683-9',
            'Camila',
            'camila@inacapmail.cl',
            '+569738539998',
            date(2004, 3, 15),
            21,
            'F',
            'CHILE',
            2022,
            550,
            4
        ))
        
        # Intentar insertar con mismo email
        success, error = db.execute_query(query, (
            '20587684-0',
            'Otro',
            'camila@inacapmail.cl',
            '+569738539999',
            date(2005, 3, 15),
            20,
            'M',
            'CHILE',
            2022,
            550,
            4
        ))
        
        assert not success, "Se permitió insertar estudiante con email duplicado"
    
    def test_estudiante_rut_duplicado(self, db):
        """Test: No permitir RUT duplicados"""
        query = """INSERT INTO Estudiante 
                  (rut, nombre, email_institucional, telefono, fecha_nacimiento, edad, sexo, nacionalidad, ano_egreso_media, puntaje_psu, integrantes_grupo_familiar) 
                  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        
        # Insertar primer estudiante
        db.execute_query(query, (
            '20587683-9',
            'Camila',
            'camila@inacapmail.cl',
            '+569738539998',
            date(2004, 3, 15),
            21,
            'F',
            'CHILE',
            2022,
            550,
            4
        ))
        
        # Intentar insertar con mismo RUT
        success, error = db.execute_query(query, (
            '20587683-9',
            'Otro',
            'otro@inacapmail.cl',
            '+569738539999',
            date(2005, 3, 15),
            20,
            'M',
            'CHILE',
            2022,
            550,
            4
        ))
        
        assert not success, "Se permitió insertar estudiante con RUT duplicado"
    
    def test_colegio_rbd_duplicado(self, db):
        """Test: No permitir RBD duplicados"""
        # Preparar datos
        db.execute_query("INSERT INTO Region (codigo, nombre) VALUES (%s, %s)", (11, 'Aysén'))
        db.execute_query("INSERT INTO Comuna (id_region, codigo, nombre) VALUES (%s, %s, %s)", 
                        (1, 1001, 'Coyhaique'))
        
        # Insertar primer colegio
        db.execute_query("""INSERT INTO Colegio (id_comuna, id_region, rbd, nombre, tipo_colegio) 
                          VALUES (%s, %s, %s, %s, %s)""",
                        (1, 1, '24206-3', 'Colegio 1', 'PARTICULARES PAGADOS'))
        
        # Intentar insertar con mismo RBD
        query = """INSERT INTO Colegio (id_comuna, id_region, rbd, nombre, tipo_colegio) 
                  VALUES (%s, %s, %s, %s, %s)"""
        success, error = db.execute_query(query, 
                                         (1, 1, '24206-3', 'Colegio 2', 'PARTICULARES PAGADOS'))
        
        assert not success, "Se permitió insertar colegio con RBD duplicado"


# ===== TESTS DE CASCADE Y RESTRICT =====

class TestConstraintsCascadeRestrict:
    """Pruebas de funcionamiento de CASCADE y RESTRICT en eliminaciones"""
    
    def test_restrict_eliminar_region_con_comunas(self, db):
        """Test: No se puede eliminar región que tiene comunas (RESTRICT)"""
        # Preparar datos
        db.execute_query("INSERT INTO Region (codigo, nombre) VALUES (%s, %s)", (11, 'Aysén'))
        db.execute_query("INSERT INTO Comuna (id_region, codigo, nombre) VALUES (%s, %s, %s)", 
                        (1, 1001, 'Coyhaique'))
        
        # Intentar eliminar región
        success, error = db.execute_query("DELETE FROM Region WHERE id_region = 1")
        
        assert not success, "Se permitió eliminar región que tiene comunas"
        assert "FOREIGN KEY" in error or "foreign key" in error.lower(), f"Error inesperado: {error}"
        
        # Verificar que la región sigue existiendo
        result = db.fetch_query("SELECT COUNT(*) FROM Region")
        assert result[0][0] == 1, "La región fue eliminada"
    
    def test_restrict_eliminar_comuna_con_colegios(self, db):
        """Test: No se puede eliminar comuna que tiene colegios (RESTRICT)"""
        # Preparar datos
        db.execute_query("INSERT INTO Region (codigo, nombre) VALUES (%s, %s)", (11, 'Aysén'))
        db.execute_query("INSERT INTO Comuna (id_region, codigo, nombre) VALUES (%s, %s, %s)", 
                        (1, 1001, 'Coyhaique'))
        db.execute_query("""INSERT INTO Colegio (id_comuna, id_region, rbd, nombre, tipo_colegio) 
                          VALUES (%s, %s, %s, %s, %s)""",
                        (1, 1, '24206-3', 'Colegio', 'PARTICULARES PAGADOS'))
        
        # Intentar eliminar comuna
        success, error = db.execute_query("DELETE FROM Comuna WHERE id_comuna = 1")
        
        assert not success, "Se permitió eliminar comuna que tiene colegios"
        
        # Verificar que la comuna sigue existiendo
        result = db.fetch_query("SELECT COUNT(*) FROM Comuna")
        assert result[0][0] == 1, "La comuna fue eliminada"
    
    def test_cascade_eliminar_estudiante_elimina_historial(self, db):
        """Test: Al eliminar estudiante se elimina su historial (CASCADE)"""
        # Insertar estudiante
        db.execute_query("""INSERT INTO Estudiante 
                          (rut, nombre, email_institucional, telefono, fecha_nacimiento, edad, sexo, nacionalidad, ano_egreso_media, puntaje_psu, integrantes_grupo_familiar) 
                          VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                        ('20587683-9', 'Camila', 'camila@inacapmail.cl', '+569738539998', 
                         date(2004, 3, 15), 21, 'F', 'CHILE', 2022, 550, 4))
        
        # Insertar historial institucional
        db.execute_query("""INSERT INTO HistorialInstitucional 
                          (id_estudiante, institucion_anterior, carrera_anterior, año_inicio, año_finalizacion) 
                          VALUES (%s, %s, %s, %s, %s)""",
                        (1, 'Universidad XYZ', 'Ingeniería', 2020, 2022))
        
        # Verificar que existe el historial
        result = db.fetch_query("SELECT COUNT(*) FROM HistorialInstitucional")
        assert result[0][0] == 1, "No se insertó el historial"
        
        # Eliminar estudiante
        success, error = db.execute_query("DELETE FROM Estudiante WHERE id_estudiante = 1")
        assert success, f"Error al eliminar estudiante: {error}"
        
        # Verificar que el historial fue eliminado (CASCADE)
        result = db.fetch_query("SELECT COUNT(*) FROM HistorialInstitucional")
        assert result[0][0] == 0, "El historial no fue eliminado al eliminar estudiante (CASCADE falló)"
    
    def test_cascade_eliminar_estudiante_colegio(self, db):
        """Test: Al eliminar estudiante se elimina la relación estudiante_colegio (CASCADE)"""
        # Preparar datos
        db.execute_query("INSERT INTO Region (codigo, nombre) VALUES (%s, %s)", (11, 'Aysén'))
        db.execute_query("INSERT INTO Comuna (id_region, codigo, nombre) VALUES (%s, %s, %s)", 
                        (1, 1001, 'Coyhaique'))
        db.execute_query("""INSERT INTO Colegio (id_comuna, id_region, rbd, nombre, tipo_colegio) 
                          VALUES (%s, %s, %s, %s, %s)""",
                        (1, 1, '24206-3', 'Colegio', 'PARTICULARES PAGADOS'))
        
        # Insertar estudiante
        db.execute_query("""INSERT INTO Estudiante 
                          (rut, nombre, email_institucional, telefono, fecha_nacimiento, edad, sexo, nacionalidad, ano_egreso_media, puntaje_psu, integrantes_grupo_familiar) 
                          VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                        ('20587683-9', 'Camila', 'camila@inacapmail.cl', '+569738539998', 
                         date(2004, 3, 15), 21, 'F', 'CHILE', 2022, 550, 4))
        
        # Insertar relación estudiante_colegio
        db.execute_query("""INSERT INTO estudiante_colegio (id_estudiante, id_colegio, ano_inicio, ano_fin) 
                          VALUES (%s, %s, %s, %s)""",
                        (1, 1, 2019, 2023))
        
        # Verificar que existe la relación
        result = db.fetch_query("SELECT COUNT(*) FROM estudiante_colegio")
        assert result[0][0] == 1, "No se insertó la relación estudiante_colegio"
        
        # Eliminar estudiante
        success, error = db.execute_query("DELETE FROM Estudiante WHERE id_estudiante = 1")
        assert success, f"Error al eliminar estudiante: {error}"
        
        # Verificar que la relación fue eliminada (CASCADE)
        result = db.fetch_query("SELECT COUNT(*) FROM estudiante_colegio")
        assert result[0][0] == 0, "La relación no fue eliminada al eliminar estudiante (CASCADE falló)"
    
    def test_restrict_eliminar_colegio_con_estudiantes(self, db):
        """Test: No se puede eliminar colegio que tiene estudiantes (RESTRICT)"""
        # Preparar datos
        db.execute_query("INSERT INTO Region (codigo, nombre) VALUES (%s, %s)", (11, 'Aysén'))
        db.execute_query("INSERT INTO Comuna (id_region, codigo, nombre) VALUES (%s, %s, %s)", 
                        (1, 1001, 'Coyhaique'))
        db.execute_query("""INSERT INTO Colegio (id_comuna, id_region, rbd, nombre, tipo_colegio) 
                          VALUES (%s, %s, %s, %s, %s)""",
                        (1, 1, '24206-3', 'Colegio', 'PARTICULARES PAGADOS'))
        
        # Insertar estudiante
        db.execute_query("""INSERT INTO Estudiante 
                          (rut, nombre, email_institucional, telefono, fecha_nacimiento, edad, sexo, nacionalidad, ano_egreso_media, puntaje_psu, integrantes_grupo_familiar) 
                          VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                        ('20587683-9', 'Camila', 'camila@inacapmail.cl', '+569738539998', 
                         date(2004, 3, 15), 21, 'F', 'CHILE', 2022, 550, 4))
        
        # Insertar relación estudiante_colegio
        db.execute_query("""INSERT INTO estudiante_colegio (id_estudiante, id_colegio, ano_inicio, ano_fin) 
                          VALUES (%s, %s, %s, %s)""",
                        (1, 1, 2019, 2023))
        
        # Intentar eliminar colegio
        success, error = db.execute_query("DELETE FROM Colegio WHERE id_colegio = 1")
        
        assert not success, "Se permitió eliminar colegio que tiene estudiantes"
        
        # Verificar que el colegio sigue existiendo
        result = db.fetch_query("SELECT COUNT(*) FROM Colegio")
        assert result[0][0] == 1, "El colegio fue eliminado"


if __name__ == "__main__":
    # Ejecutar con: pytest test_database.py -v -s
    pytest.main([__file__, "-v", "-s"])
