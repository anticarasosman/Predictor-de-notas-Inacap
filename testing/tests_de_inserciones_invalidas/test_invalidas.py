"""
Tests de inserciones inválidas en la base de datos
Verifica que se RECHACEN correctamente inserciones inválidas y duplicadas
"""

import pytest
from datetime import date


class TestInsertarDatosInvalidos:
    """Pruebas de inserciones inválidas (deben fallar)"""
    
    def test_region_codigo_duplicado(self, db):
        """Test: No permitir códigos de región duplicados"""
        # Insertar primera región
        success, error = db.execute_query("INSERT INTO Region (codigo, nombre) VALUES (%s, %s)", 
                        (11, 'Aysén'))
        assert success, f"Error al insertar region: {error}"
        
        # Intentar insertar con mismo código
        query = "INSERT INTO Region (codigo, nombre) VALUES (%s, %s)"
        success, error = db.execute_query(query, (11, 'Otra Región'))
        
        assert not success, "Se permitió insertar región con código duplicado"
        assert "UNIQUE" in error or "duplicate" in error.lower(), f"Error inesperado: {error}"
    
    def test_region_nombre_duplicado(self, db):
        """Test: No permitir nombres de región duplicados"""
        # Insertar primera región
        success, error = db.execute_query("INSERT INTO Region (codigo, nombre) VALUES (%s, %s)", 
                        (11, 'Aysén'))
        assert success, f"Error al insertar region: {error}"
        
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
        success, error = db.execute_query("INSERT INTO Region (codigo, nombre) VALUES (%s, %s)", (11, 'Aysén'))
        assert success, f"Error al insertar region: {error}"
        
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
        success, error = db.execute_query(query, (
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
        assert success, f"Error al insertar estudiante base: {error}"
        
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
        success, error = db.execute_query(query, (
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
        assert success, f"Error al insertar estudiante base: {error}"
        
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
        success, error = db.execute_query("INSERT INTO Region (codigo, nombre) VALUES (%s, %s)", (11, 'Aysén'))
        assert success, f"Error al insertar region: {error}"
        success, error = db.execute_query("INSERT INTO Comuna (id_region, codigo, nombre) VALUES (%s, %s, %s)", 
                (1, 1001, 'Coyhaique'))
        assert success, f"Error al insertar comuna: {error}"
        
        # Insertar primer colegio
        success, error = db.execute_query("""INSERT INTO Colegio (id_comuna, id_region, rbd, nombre, tipo_colegio) 
                  VALUES (%s, %s, %s, %s, %s)""",
                (1, 1, '24206-3', 'Colegio 1', 'PARTICULARES PAGADOS'))
        assert success, f"Error al insertar colegio base: {error}"
        
        # Intentar insertar con mismo RBD
        query = """INSERT INTO Colegio (id_comuna, id_region, rbd, nombre, tipo_colegio) 
                  VALUES (%s, %s, %s, %s, %s)"""
        success, error = db.execute_query(query, 
                                         (1, 1, '24206-3', 'Colegio 2', 'PARTICULARES PAGADOS'))
        
        assert not success, "Se permitió insertar colegio con RBD duplicado"
