"""
Tests de inserciones válidas en la base de datos
Verifica que se pueden insertar correctamente datos válidos
"""

import pytest
from datetime import date


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
        success, error = db.execute_query("INSERT INTO Region (codigo, nombre) VALUES (%s, %s)", 
                        (11, 'Aysén'))
        assert success, f"Error al insertar region: {error}"
        
        # Insertar comuna
        query = "INSERT INTO Comuna (id_region, codigo, nombre) VALUES (%s, %s, %s)"
        success, error = db.execute_query(query, (1, 1001, 'Coyhaique'))
        
        assert success, f"Error al insertar comuna: {error}"
    
    def test_insertar_colegio_completo(self, db):
        """Test: Insertar colegio con región y comuna"""
        # Insertar región
        success, error = db.execute_query("INSERT INTO Region (codigo, nombre) VALUES (%s, %s)", 
                (11, 'Aysén'))
        assert success, f"Error al insertar region: {error}"
        
        # Insertar comuna
        success, error = db.execute_query("INSERT INTO Comuna (id_region, codigo, nombre) VALUES (%s, %s, %s)", 
                (1, 1001, 'Coyhaique'))
        assert success, f"Error al insertar comuna: {error}"
        
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
        success, error = db.execute_query("""INSERT INTO Estudiante 
                  (rut, nombre, email_institucional, telefono, fecha_nacimiento, edad, sexo, nacionalidad, ano_egreso_media, puntaje_psu, integrantes_grupo_familiar) 
                  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                ('20587683-9', 'Camila', 'camila@inacapmail.cl', '+569738539998', 
                 date(2004, 3, 15), 21, 'F', 'CHILE', 2022, 550, 4))
        assert success, f"Error al insertar estudiante: {error}"
        
        # Insertar región y comuna
        success, error = db.execute_query("INSERT INTO Region (codigo, nombre) VALUES (%s, %s)", (11, 'Aysén'))
        assert success, f"Error al insertar region: {error}"
        success, error = db.execute_query("INSERT INTO Comuna (id_region, codigo, nombre) VALUES (%s, %s, %s)", 
                (1, 1001, 'Coyhaique'))
        assert success, f"Error al insertar comuna: {error}"
        
        # Insertar dirección
        success, error = db.execute_query("""INSERT INTO Direccion (id_comuna, calle, numero, tipo_direccion) 
                  VALUES (%s, %s, %s, %s)""",
                (1, 'Calle Principal', 123, 'Permanente'))
        assert success, f"Error al insertar direccion: {error}"
        
        # Obtener id_estudiante real
        rows = db.fetch_query("SELECT id_estudiante FROM Estudiante WHERE rut = %s", ('20587683-9',))
        assert rows and rows[0], "No se obtuvo id_estudiante"
        est_id = rows[0][0]
        
        # Insertar en tabla bridge
        query = "INSERT INTO estudiante_direccion (estudiante_id) VALUES (%s)"
        success, error = db.execute_query(query, (est_id,))
        
        assert success, f"Error al insertar en tabla bridge: {error}"
