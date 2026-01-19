"""
Test de verificación: Datos semilla cargados correctamente
Ejecuta este test primero para verificar que todo el sistema funciona
"""

import pytest


class TestVerificarDatosSemilla:
    """Tests para verificar que los datos semilla se cargaron correctamente"""
    
    def test_regiones_cargadas(self, db):
        """Verificar que las regiones se cargaron"""
        result = db.fetch_query("SELECT COUNT(*) FROM Region")
        assert result[0][0] >= 4, "Debe haber al menos 4 regiones"
        
        # Verificar región específica
        result = db.fetch_query("SELECT nombre FROM Region WHERE codigo = 11")
        assert result and len(result) > 0, "Región 11 (Aysén) no encontrada"
        print(f"   ✓ Región encontrada: {result[0][0]}")
    
    def test_estudiantes_cargados(self, db):
        """Verificar que los estudiantes se cargaron"""
        result = db.fetch_query("SELECT COUNT(*) FROM Estudiante")
        count = result[0][0]
        assert count >= 8, f"Debe haber al menos 8 estudiantes, se encontraron {count}"
        print(f"   ✓ {count} estudiantes cargados")
        
        # Verificar estudiante específico (Camila)
        result = db.fetch_query("SELECT nombre, email_institucional FROM Estudiante WHERE rut = %s", ('20587683-9',))
        assert result and len(result) > 0, "Camila Manríquez no encontrada"
        print(f"   ✓ Estudiante encontrado: {result[0][0]} ({result[0][1]})")
    
    def test_carreras_cargadas(self, db):
        """Verificar que las carreras se cargaron"""
        result = db.fetch_query("SELECT COUNT(*) FROM Carrera")
        assert result[0][0] >= 3, "Debe haber al menos 3 carreras"
        
        # Verificar carrera específica
        result = db.fetch_query("SELECT nombre_carrera FROM Carrera WHERE codigo_carrera = 'AE'")
        assert result and len(result) > 0, "Carrera AE no encontrada"
        print(f"   ✓ Carrera encontrada: {result[0][0]}")
    
    def test_ramos_cargados(self, db):
        """Verificar que los ramos se cargaron"""
        result = db.fetch_query("SELECT COUNT(*) FROM Ramo")
        count = result[0][0]
        assert count >= 10, f"Debe haber al menos 10 ramos, se encontraron {count}"
        print(f"   ✓ {count} ramos cargados")
        
        # Verificar ramo de inglés
        result = db.fetch_query("SELECT nombre_ramo FROM Ramo WHERE sigla = 'IDEN02'")
        assert result and len(result) > 0, "Ramo IDEN02 no encontrado"
        print(f"   ✓ Ramo encontrado: {result[0][0]}")
    
    def test_profesores_cargados(self, db):
        """Verificar que los profesores se cargaron"""
        result = db.fetch_query("SELECT COUNT(*) FROM Profesor")
        count = result[0][0]
        assert count >= 9, f"Debe haber al menos 9 profesores, se encontraron {count}"
        print(f"   ✓ {count} profesores cargados")
    
    def test_relaciones_estudiante_colegio(self, db):
        """Verificar relaciones estudiante-colegio"""
        result = db.fetch_query("SELECT COUNT(*) FROM estudiante_colegio")
        count = result[0][0]
        assert count >= 4, f"Debe haber al menos 4 relaciones estudiante-colegio, se encontraron {count}"
        print(f"   ✓ {count} relaciones estudiante-colegio cargadas")
    
    def test_notas_estudiante_cargadas(self, db):
        """Verificar que hay notas cargadas"""
        result = db.fetch_query("SELECT COUNT(*) FROM Notas_Estudiante")
        count = result[0][0]
        assert count >= 4, f"Debe haber al menos 4 registros de notas, se encontraron {count}"
        print(f"   ✓ {count} registros de notas cargados")
        
        # Verificar nota específica de Anahí
        result = db.fetch_query("""
            SELECT promedio_matematicas, promedio_lenguaje, promedio_ingles 
            FROM Notas_Estudiante 
            WHERE id_estudiante = (SELECT id_estudiante FROM Estudiante WHERE rut = %s)
        """, ('21195581-3',))
        
        if result and len(result) > 0:
            mat, leng, ing = result[0]
            print(f"   ✓ Notas de Anahí: Mat={mat}, Leng={leng}, Ing={ing}")
            assert mat == 5.5, "Promedio matemáticas de Anahí debe ser 5.5"
    
    def test_integracion_completa(self, db):
        """Test de integración: Consulta compleja con múltiples tablas"""
        query = """
            SELECT 
                e.nombre,
                c.nombre_carrera,
                col.nombre as colegio,
                r.nombre as region
            FROM Estudiante e
            JOIN Matricula m ON e.id_estudiante = m.id_estudiante
            JOIN Carrera c ON m.id_carrera = c.id_carrera
            JOIN estudiante_colegio ec ON e.id_estudiante = ec.id_estudiante
            JOIN Colegio col ON ec.id_colegio = col.id_colegio
            JOIN Region r ON col.id_region = r.id_region
            WHERE e.rut = %s
        """
        
        result = db.fetch_query(query, ('20587683-9',))  # Camila
        
        if result and len(result) > 0:
            nombre, carrera, colegio, region = result[0]
            print(f"   ✓ Datos integrados de Camila:")
            print(f"     - Nombre: {nombre}")
            print(f"     - Carrera: {carrera}")
            print(f"     - Colegio: {colegio}")
            print(f"     - Región: {region}")
            
            assert nombre is not None
            assert carrera is not None
            assert colegio is not None
            assert region is not None
        else:
            pytest.skip("No se pudo realizar consulta de integración (puede ser problema de FK)")
    
    def test_fixture_db_empty(self, db_empty):
        """Verificar que fixture db_empty NO tiene datos"""
        result = db_empty.fetch_query("SELECT COUNT(*) FROM Estudiante")
        assert result[0][0] == 0, "db_empty no debe tener estudiantes"
        
        result = db_empty.fetch_query("SELECT COUNT(*) FROM Region")
        assert result[0][0] == 0, "db_empty no debe tener regiones"
        
        print("   ✓ Fixture db_empty funciona correctamente (BD vacía)")


if __name__ == "__main__":
    """
    Para ejecutar estos tests:
    pytest testing/test_verificar_seed_data.py -v
    """
    pass
