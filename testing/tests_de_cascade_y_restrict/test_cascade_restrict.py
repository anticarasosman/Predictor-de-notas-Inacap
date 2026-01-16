"""
Tests de funcionamiento de CASCADE y RESTRICT en eliminaciones
Verifica que las reglas de integridad referencial funcionen correctamente
"""

import pytest
from datetime import date


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
        success, error = db.execute_query("""INSERT INTO Estudiante 
                          (rut, nombre, email_institucional, telefono, fecha_nacimiento, edad, sexo, nacionalidad, ano_egreso_media, puntaje_psu, integrantes_grupo_familiar) 
                          VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                        ('20587683-9', 'Camila', 'camila@inacapmail.cl', '+569738539998', 
                         date(2004, 3, 15), 21, 'F', 'CHILE', 2022, 550, 4))
        assert success, f"Error al insertar estudiante: {error}"

        # Obtener id_estudiante real
        rows = db.fetch_query("SELECT id_estudiante FROM Estudiante WHERE rut = %s", ('20587683-9',))
        assert rows and rows[0], "No se obtuvo id_estudiante"
        est_id = rows[0][0]
        
        # Insertar historial institucional
        success, error = db.execute_query("""INSERT INTO HistorialInstitucional 
                          (id_estudiante, institucion_anterior, carrera_anterior, ano_inicio, ano_finalizacion) 
                          VALUES (%s, %s, %s, %s, %s)""",
                        (est_id, 'Universidad XYZ', 'Ingeniería', 2020, 2022))
        assert success, f"Error al insertar historial: {error}"
        
        # Verificar que existe el historial
        result = db.fetch_query("SELECT COUNT(*) FROM HistorialInstitucional")
        assert result is not None and result[0][0] == 1, "No se insertó el historial"
        
        # Eliminar estudiante
        success, error = db.execute_query("DELETE FROM Estudiante WHERE id_estudiante = %s", (est_id,))
        assert success, f"Error al eliminar estudiante: {error}"
        
        # Verificar que el historial fue eliminado (CASCADE)
        result = db.fetch_query("SELECT COUNT(*) FROM HistorialInstitucional")
        assert result is not None and result[0][0] == 0, "El historial no fue eliminado al eliminar estudiante (CASCADE falló)"
    
    def test_cascade_eliminar_estudiante_colegio(self, db):
        """Test: Al eliminar estudiante se elimina la relación estudiante_colegio (CASCADE)"""
        # Preparar datos
        success, error = db.execute_query("INSERT INTO Region (codigo, nombre) VALUES (%s, %s)", (11, 'Aysén'))
        assert success, f"Error al insertar region: {error}"
        success, error = db.execute_query("INSERT INTO Comuna (id_region, codigo, nombre) VALUES (%s, %s, %s)", 
                        (1, 1001, 'Coyhaique'))
        assert success, f"Error al insertar comuna: {error}"
        success, error = db.execute_query("""INSERT INTO Colegio (id_comuna, id_region, rbd, nombre, tipo_colegio) 
                          VALUES (%s, %s, %s, %s, %s)""",
                        (1, 1, '24206-3', 'Colegio', 'PARTICULARES PAGADOS'))
        assert success, f"Error al insertar colegio: {error}"
        
        # Insertar estudiante
        success, error = db.execute_query("""INSERT INTO Estudiante 
                          (rut, nombre, email_institucional, telefono, fecha_nacimiento, edad, sexo, nacionalidad, ano_egreso_media, puntaje_psu, integrantes_grupo_familiar) 
                          VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                        ('20587683-9', 'Camila', 'camila@inacapmail.cl', '+569738539998', 
                         date(2004, 3, 15), 21, 'F', 'CHILE', 2022, 550, 4))
        assert success, f"Error al insertar estudiante: {error}"

        rows = db.fetch_query("SELECT id_estudiante FROM Estudiante WHERE rut = %s", ('20587683-9',))
        assert rows and rows[0], "No se obtuvo id_estudiante"
        est_id = rows[0][0]
        
        # Insertar relación estudiante_colegio
        success, error = db.execute_query("""INSERT INTO estudiante_colegio (id_estudiante, id_colegio, ano_inicio, ano_fin) 
                          VALUES (%s, %s, %s, %s)""",
                        (est_id, 1, 2019, 2023))
        assert success, f"Error al insertar estudiante_colegio: {error}"
        
        # Verificar que existe la relación
        result = db.fetch_query("SELECT COUNT(*) FROM estudiante_colegio")
        assert result[0][0] == 1, "No se insertó la relación estudiante_colegio"
        
        # Eliminar estudiante
        success, error = db.execute_query("DELETE FROM Estudiante WHERE id_estudiante = %s", (est_id,))
        assert success, f"Error al eliminar estudiante: {error}"
        
        # Verificar que la relación fue eliminada (CASCADE)
        result = db.fetch_query("SELECT COUNT(*) FROM estudiante_colegio")
        assert result[0][0] == 0, "La relación no fue eliminada al eliminar estudiante (CASCADE falló)"
    
    def test_restrict_eliminar_colegio_con_estudiantes(self, db):
        """Test: No se puede eliminar colegio que tiene estudiantes (RESTRICT)"""
        # Preparar datos
        success, error = db.execute_query("INSERT INTO Region (codigo, nombre) VALUES (%s, %s)", (11, 'Aysén'))
        assert success, f"Error al insertar region: {error}"
        success, error = db.execute_query("INSERT INTO Comuna (id_region, codigo, nombre) VALUES (%s, %s, %s)", 
                        (1, 1001, 'Coyhaique'))
        assert success, f"Error al insertar comuna: {error}"
        success, error = db.execute_query("""INSERT INTO Colegio (id_comuna, id_region, rbd, nombre, tipo_colegio) 
                          VALUES (%s, %s, %s, %s, %s)""",
                        (1, 1, '24206-3', 'Colegio', 'PARTICULARES PAGADOS'))
        assert success, f"Error al insertar colegio: {error}"
        
        # Insertar estudiante
        success, error = db.execute_query("""INSERT INTO Estudiante 
                          (rut, nombre, email_institucional, telefono, fecha_nacimiento, edad, sexo, nacionalidad, ano_egreso_media, puntaje_psu, integrantes_grupo_familiar) 
                          VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                        ('20587683-9', 'Camila', 'camila@inacapmail.cl', '+569738539998', 
                         date(2004, 3, 15), 21, 'F', 'CHILE', 2022, 550, 4))
        assert success, f"Error al insertar estudiante: {error}"

        rows = db.fetch_query("SELECT id_estudiante FROM Estudiante WHERE rut = %s", ('20587683-9',))
        assert rows and rows[0], "No se obtuvo id_estudiante"
        est_id = rows[0][0]
        
        # Insertar relación estudiante_colegio
        success, error = db.execute_query("""INSERT INTO estudiante_colegio (id_estudiante, id_colegio, ano_inicio, ano_fin) 
                          VALUES (%s, %s, %s, %s)""",
                        (est_id, 1, 2019, 2023))
        assert success, f"Error al insertar estudiante_colegio: {error}"
        
        # Intentar eliminar colegio
        success, error = db.execute_query("DELETE FROM Colegio WHERE id_colegio = 1")
        
        assert not success, "Se permitió eliminar colegio que tiene estudiantes"
        
        # Verificar que el colegio sigue existiendo
        result = db.fetch_query("SELECT COUNT(*) FROM Colegio")
        assert result[0][0] == 1, "El colegio fue eliminado"
