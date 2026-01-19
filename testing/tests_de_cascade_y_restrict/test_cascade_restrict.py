"""
Tests de funcionamiento de CASCADE y RESTRICT en eliminaciones
Verifica que las reglas de integridad referencial funcionen correctamente

NOTA: Los tests usan datos semilla precargados para mayor eficiencia.
"""

import pytest
from datetime import date


class TestConstraintsCascadeRestrict:
    """Pruebas de funcionamiento de CASCADE y RESTRICT en eliminaciones"""
    
    def test_restrict_eliminar_region_con_comunas(self, db):
        """Test: No se puede eliminar región que tiene comunas (RESTRICT)"""
        # Región 11 (Aysén) ya tiene comunas en datos semilla
        result = db.fetch_query("SELECT id_region FROM Region WHERE codigo = %s", (11,))
        assert result and len(result) > 0, "Región no encontrada"
        id_region = result[0][0]
        
        # Intentar eliminar región
        success, error = db.execute_query(f"DELETE FROM Region WHERE id_region = {id_region}")
        
        assert not success, "Se permitió eliminar región que tiene comunas"
        assert "FOREIGN KEY" in error or "foreign key" in error.lower(), f"Error inesperado: {error}"
        
        # Verificar que la región sigue existiendo
        result = db.fetch_query("SELECT COUNT(*) FROM Region WHERE id_region = %s", (id_region,))
        assert result[0][0] == 1, "La región fue eliminada"
    
    def test_restrict_eliminar_comuna_con_colegios(self, db):
        """Test: No se puede eliminar comuna que tiene colegios (RESTRICT)"""
        # Coyhaique ya tiene colegios en datos semilla
        result = db.fetch_query("SELECT id_comuna FROM Comuna WHERE nombre = %s", ('Coyhaique',))
        assert result and len(result) > 0, "Comuna no encontrada"
        id_comuna = result[0][0]
        
        # Intentar eliminar comuna
        success, error = db.execute_query(f"DELETE FROM Comuna WHERE id_comuna = {id_comuna}")
        
        assert not success, "Se permitió eliminar comuna que tiene colegios"
        
        # Verificar que la comuna sigue existiendo
        result = db.fetch_query("SELECT COUNT(*) FROM Comuna WHERE id_comuna = %s", (id_comuna,))
        assert result[0][0] == 1, "La comuna fue eliminada"
    
    def test_cascade_eliminar_estudiante_elimina_historial(self, db):
        """Test: Al eliminar estudiante se elimina su historial (CASCADE)"""
        # Camila ya tiene historial en datos semilla
        result = db.fetch_query("SELECT id_estudiante FROM Estudiante WHERE rut = %s", ('20587683-9',))
        assert result and len(result) > 0, "Camila no encontrada"
        est_id = result[0][0]
        
        # Verificar que tiene historial
        result = db.fetch_query("SELECT COUNT(*) FROM HistorialInstitucional WHERE id_estudiante = %s", (est_id,))
        historial_count_antes = result[0][0]
        assert historial_count_antes > 0, "Camila no tiene historial en datos semilla"
        
        # Eliminar estudiante
        success, error = db.execute_query("DELETE FROM Estudiante WHERE id_estudiante = %s", (est_id,))
        assert success, f"Error al eliminar estudiante: {error}"
        
        # Verificar que el historial fue eliminado (CASCADE)
        result = db.fetch_query("SELECT COUNT(*) FROM HistorialInstitucional WHERE id_estudiante = %s", (est_id,))
        assert result[0][0] == 0, "El historial no fue eliminado al eliminar estudiante (CASCADE falló)"
    
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
    
    def test_cascade_eliminar_estudiante_elimina_direccion(self, db):
        """Test: Al eliminar estudiante se elimina su relación con direcciones (CASCADE)"""
        # Preparar datos
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
        
        # Insertar relación estudiante_direccion
        success, error = db.execute_query("""INSERT INTO estudiante_direccion (id_estudiante, id_direccion) 
                          VALUES (%s, %s)""",
                        (est_id, 1))
        assert success, f"Error al insertar estudiante_direccion: {error}"
        
        # Verificar que existe la relación
        result = db.fetch_query("SELECT COUNT(*) FROM estudiante_direccion")
        assert result[0][0] == 1, "No se insertó la relación estudiante_direccion"
        
        # Eliminar estudiante
        success, error = db.execute_query("DELETE FROM Estudiante WHERE id_estudiante = %s", (est_id,))
        assert success, f"Error al eliminar estudiante: {error}"
        
        # Verificar que la relación fue eliminada (CASCADE)
        result = db.fetch_query("SELECT COUNT(*) FROM estudiante_direccion")
        assert result[0][0] == 0, "La relación no fue eliminada al eliminar estudiante (CASCADE falló)"
    
    def test_cascade_eliminar_direccion_elimina_estudiante_direccion(self, db):
        """Test: Al eliminar dirección se elimina su relación con estudiantes (CASCADE)"""
        # Preparar datos
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
        
        # Insertar relación estudiante_direccion
        success, error = db.execute_query("""INSERT INTO estudiante_direccion (id_estudiante, id_direccion) 
                          VALUES (%s, %s)""",
                        (est_id, 1))
        assert success, f"Error al insertar estudiante_direccion: {error}"
        
        # Verificar que existe la relación
        result = db.fetch_query("SELECT COUNT(*) FROM estudiante_direccion")
        assert result[0][0] == 1, "No se insertó la relación estudiante_direccion"
        
        # Eliminar dirección
        success, error = db.execute_query("DELETE FROM Direccion WHERE id_direccion = 1")
        assert success, f"Error al eliminar direccion: {error}"
        
        # Verificar que la relación fue eliminada (CASCADE)
        result = db.fetch_query("SELECT COUNT(*) FROM estudiante_direccion")
        assert result[0][0] == 0, "La relación no fue eliminada al eliminar dirección (CASCADE falló)"
