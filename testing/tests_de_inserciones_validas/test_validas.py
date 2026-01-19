"""
Tests de inserciones válidas en la base de datos
Verifica que se pueden insertar correctamente datos válidos

NOTA: Los tests ahora usan datos semilla precargados para mayor eficiencia.
Para tests que requieran BD vacía, usa fixture db_empty.
"""

import pytest
from datetime import date


class TestInsertarDatosValidos:
    """Pruebas de inserciones válidas en la base de datos"""
    
    def test_verificar_datos_semilla_cargados(self, db):
        """Test: Verificar que los datos semilla se cargaron correctamente"""
        # Verificar regiones
        result = db.fetch_query("SELECT COUNT(*) FROM Region")
        assert result[0][0] >= 4, "No se cargaron las regiones semilla"
        
        # Verificar estudiantes
        result = db.fetch_query("SELECT COUNT(*) FROM Estudiante")
        assert result[0][0] >= 8, "No se cargaron los estudiantes semilla"
        
        # Verificar que Camila existe
        result = db.fetch_query("SELECT nombre FROM Estudiante WHERE rut = %s", ('20587683-9',))
        assert result and len(result) > 0, "Camila Manríquez no está en datos semilla"
    
    def test_insertar_region(self, db):
        """Test: Insertar una región válida adicional"""
        query = "INSERT INTO Region (codigo, nombre) VALUES (%s, %s)"
        success, error = db.execute_query(query, (10, 'Los Lagos'))
        
        assert success, f"Error al insertar región: {error}"
        
        # Verificar que se insertó
        result = db.fetch_query("SELECT * FROM Region WHERE codigo = 10")
        assert result is not None and len(result) > 0, "Región no encontrada después de insertar"
        assert result[0][2] == 'Los Lagos'
    
    def test_insertar_multiple_regiones(self, db):
        """Test: Insertar múltiples regiones adicionales"""
        regions = [
            (10, 'Los Lagos'),
            (14, 'Los Ríos'),
            (15, 'Arica y Parinacota'),
        ]
        
        for codigo, nombre in regions:
            query = "INSERT INTO Region (codigo, nombre) VALUES (%s, %s)"
            success, error = db.execute_query(query, (codigo, nombre))
            assert success, f"Error al insertar región {nombre}: {error}"
        
        # Verificar que se insertaron (deben haber al menos 7: 4 semilla + 3 nuevas)
        result = db.fetch_query("SELECT COUNT(*) FROM Region")
        assert result[0][0] >= 7, "No se insertaron todas las regiones"
    
    def test_usar_comuna_existente(self, db):
        """Test: Usar comuna de datos semilla para insertar colegio"""
        # Coyhaique ya existe en datos semilla
        result = db.fetch_query("SELECT id_comuna, id_region FROM Comuna WHERE nombre = %s", ('Coyhaique',))
        assert result and len(result) > 0, "Comuna Coyhaique no encontrada en datos semilla"
        
        id_comuna, id_region = result[0]
        
        # Insertar nuevo colegio usando comuna existente
        query = """INSERT INTO Colegio (id_comuna, id_region, rbd, nombre, tipo_colegio) 
                  VALUES (%s, %s, %s, %s, %s)"""
        success, error = db.execute_query(query, 
                                         (id_comuna, id_region, '99999-9', 'Colegio Nuevo Test', 'PARTICULARES PAGADOS'))
        
        assert success, f"Error al insertar colegio con comuna existente: {error}"
    
    def test_insertar_estudiante(self, db):
        """Test: Insertar un estudiante válido adicional"""
        query = """INSERT INTO Estudiante 
                  (rut, nombre, email_institucional, telefono, fecha_nacimiento, edad, sexo, nacionalidad, ano_egreso_media, puntaje_psu, integrantes_grupo_familiar) 
                  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        
        success, error = db.execute_query(query, (
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
            3
        ))
        
        assert success, f"Error al insertar estudiante: {error}"
        
        # Verificar que se insertó
        result = db.fetch_query("SELECT COUNT(*) FROM Estudiante WHERE rut = %s", ('99999999-9',))
        assert result[0][0] == 1, "Estudiante no encontrado"
    
    def test_usar_estudiante_existente_para_historial(self, db):
        """Test: Usar estudiante de datos semilla para crear historial"""
        # Camila ya existe con id_estudiante
        result = db.fetch_query("SELECT id_estudiante FROM Estudiante WHERE rut = %s", ('20587683-9',))
        assert result and len(result) > 0, "Camila no encontrada en datos semilla"
        
        id_estudiante = result[0][0]
        
        # Insertar historial nuevo para Camila
        query = """INSERT INTO HistorialInstitucional 
                  (id_estudiante, institucion_anterior, carrera_anterior, ano_inicio, ano_finalizacion) 
                  VALUES (%s, %s, %s, %s, %s)"""
        success, error = db.execute_query(query, 
                                         (id_estudiante, 'Universidad Test', 'Ingeniería Test', 2018, 2020))
        
        assert success, f"Error al insertar historial: {error}"
