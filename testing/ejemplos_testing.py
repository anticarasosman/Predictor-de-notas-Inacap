"""
EJEMPLOS DE USO DE TESTING
===========================

Este archivo contiene ejemplos prácticos de cómo usar el testing.
Puedes copiar y adaptar estos ejemplos para tus propias pruebas.
"""

from testing.test_database import DatabaseManager
from datetime import date


def ejemplo_1_insertar_datos_validos():
    """
    Ejemplo 1: Insertar datos válidos en la BD
    """
    print("\n" + "="*60)
    print("EJEMPLO 1: Insertar datos válidos")
    print("="*60)
    
    db = DatabaseManager()
    db.connect()
    db.clear_tables()
    
    # Insertar una región
    print("\n1. Insertando región...")
    success, error = db.execute_query(
        "INSERT INTO Region (codigo, nombre) VALUES (%s, %s)",
        (11, 'Aysén del General Carlos Ibáñez del Campo')
    )
    
    if success:
        print("   ✓ Región insertada correctamente")
    else:
        print(f"   ✗ Error: {error}")
    
    # Insertar una comuna
    print("\n2. Insertando comuna...")
    success, error = db.execute_query(
        "INSERT INTO Comuna (id_region, codigo, nombre) VALUES (%s, %s, %s)",
        (1, 1001, 'Coyhaique')
    )
    
    if success:
        print("   ✓ Comuna insertada correctamente")
    else:
        print(f"   ✗ Error: {error}")
    
    # Verificar datos insertados
    print("\n3. Verificando datos insertados...")
    result = db.fetch_query("SELECT * FROM Region")
    print(f"   Regiones en BD: {len(result) if result else 0}")
    if result:
        for row in result:
            print(f"   - ID: {row[0]}, Código: {row[1]}, Nombre: {row[2]}")
    
    db.disconnect()


def ejemplo_2_intentar_insertar_invalido():
    """
    Ejemplo 2: Intentar insertar datos inválidos
    """
    print("\n" + "="*60)
    print("EJEMPLO 2: Intentar insertar datos inválidos")
    print("="*60)
    
    db = DatabaseManager()
    db.connect()
    db.clear_tables()
    
    # Insertar región
    print("\n1. Insertando región válida...")
    success, error = db.execute_query(
        "INSERT INTO Region (codigo, nombre) VALUES (%s, %s)",
        (11, 'Aysén')
    )
    print(f"   {'✓' if success else '✗'} {error if not success else 'Región insertada'}")
    
    # Intentar insertar región con mismo código
    print("\n2. Intentando insertar región con código DUPLICADO...")
    success, error = db.execute_query(
        "INSERT INTO Region (codigo, nombre) VALUES (%s, %s)",
        (11, 'Otra región')
    )
    
    if not success:
        print(f"   ✓ Validación funcionó correctamente")
        print(f"   Error: {error[:80]}...")
    else:
        print(f"   ✗ ERROR: Se permitió insertar código duplicado!")
    
    # Intentar insertar comuna sin región válida
    print("\n3. Intentando insertar COMUNA sin región válida...")
    success, error = db.execute_query(
        "INSERT INTO Comuna (id_region, codigo, nombre) VALUES (%s, %s, %s)",
        (999, 1001, 'Comuna')  # id_region 999 no existe
    )
    
    if not success:
        print(f"   ✓ Validación de foreign key funcionó")
        print(f"   Error: {error[:80]}...")
    else:
        print(f"   ✗ ERROR: Se permitió insertar comuna sin región!")
    
    db.disconnect()


def ejemplo_3_cascade_eliminacion():
    """
    Ejemplo 3: Probar CASCADE al eliminar
    """
    print("\n" + "="*60)
    print("EJEMPLO 3: Probar CASCADE en eliminaciones")
    print("="*60)
    
    db = DatabaseManager()
    db.connect()
    db.clear_tables()
    
    # Preparar datos
    print("\n1. Preparando datos...")
    db.execute_query(
        "INSERT INTO Estudiante (rut, nombre, email_institucional, telefono, fecha_nacimiento, edad, sexo, nacionalidad, ano_egreso_media, puntaje_psu, integrantes_grupo_familiar) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
        ('20587683-9', 'Camila', 'camila@inacapmail.cl', '+569738539998', date(2004, 3, 15), 21, 'F', 'CHILE', 2022, 550, 4)
    )
    
    db.execute_query(
        "INSERT INTO HistorialInstitucional (id_estudiante, institucion_anterior, carrera_anterior, año_inicio, año_finalizacion) VALUES (%s, %s, %s, %s, %s)",
        (1, 'Universidad XYZ', 'Ingeniería', 2020, 2022)
    )
    print("   ✓ Datos preparados")
    
    # Verificar existencia
    print("\n2. Verificando que existen los registros...")
    result = db.fetch_query("SELECT COUNT(*) FROM Estudiante")
    est_count = result[0][0]
    result = db.fetch_query("SELECT COUNT(*) FROM HistorialInstitucional")
    hist_count = result[0][0]
    print(f"   Estudiantes: {est_count}")
    print(f"   Historiales: {hist_count}")
    
    # Eliminar estudiante
    print("\n3. Eliminando estudiante (debe eliminar también el historial por CASCADE)...")
    success, error = db.execute_query("DELETE FROM Estudiante WHERE id_estudiante = 1")
    print(f"   ✓ Estudiante eliminado")
    
    # Verificar eliminación en cascada
    print("\n4. Verificando CASCADE...")
    result = db.fetch_query("SELECT COUNT(*) FROM Estudiante")
    est_count = result[0][0]
    result = db.fetch_query("SELECT COUNT(*) FROM HistorialInstitucional")
    hist_count = result[0][0]
    print(f"   Estudiantes en BD: {est_count}")
    print(f"   Historiales en BD: {hist_count}")
    
    if est_count == 0 and hist_count == 0:
        print("   ✓ CASCADE funcionó correctamente!")
    else:
        print("   ✗ CASCADE NO funcionó!")
    
    db.disconnect()


def ejemplo_4_restrict_eliminacion():
    """
    Ejemplo 4: Probar RESTRICT al eliminar
    """
    print("\n" + "="*60)
    print("EJEMPLO 4: Probar RESTRICT en eliminaciones")
    print("="*60)
    
    db = DatabaseManager()
    db.connect()
    db.clear_tables()
    
    # Preparar datos
    print("\n1. Preparando datos...")
    db.execute_query("INSERT INTO Region (codigo, nombre) VALUES (%s, %s)", (11, 'Aysén'))
    db.execute_query("INSERT INTO Comuna (id_region, codigo, nombre) VALUES (%s, %s, %s)", (1, 1001, 'Coyhaique'))
    print("   ✓ Región y comuna creadas")
    
    # Intentar eliminar región
    print("\n2. Intentando eliminar región que tiene comunas...")
    print("   (Debe fallar por RESTRICT)")
    success, error = db.execute_query("DELETE FROM Region WHERE id_region = 1")
    
    if not success:
        print(f"   ✓ RESTRICT funcionó correctamente!")
        print(f"   Error: {error[:80]}...")
    else:
        print(f"   ✗ ERROR: Se permitió eliminar región con comunas!")
    
    # Verificar que región sigue existiendo
    print("\n3. Verificando que la región sigue existiendo...")
    result = db.fetch_query("SELECT COUNT(*) FROM Region")
    count = result[0][0]
    print(f"   Regiones en BD: {count}")
    
    if count > 0:
        print("   ✓ Región no fue eliminada (RESTRICT funcionó)")
    else:
        print("   ✗ Región fue eliminada (RESTRICT falló)")
    
    db.disconnect()


def ejemplo_5_insertar_multiples_estudiantes():
    """
    Ejemplo 5: Insertar múltiples estudiantes con datos diferentes
    """
    print("\n" + "="*60)
    print("EJEMPLO 5: Insertar múltiples estudiantes")
    print("="*60)
    
    db = DatabaseManager()
    db.connect()
    db.clear_tables()
    
    # Lista de estudiantes a insertar
    estudiantes = [
        ('20587683-9', 'Camila Manríquez', 'camila.manriquez@inacapmail.cl', '+569738539998', date(2004, 3, 15), 21, 'F', 'CHILE', 2022, 550, 4),
        ('20587684-0', 'Juan García', 'juan.garcia@inacapmail.cl', '+569738539999', date(2003, 5, 20), 22, 'M', 'CHILE', 2021, 600, 5),
        ('20587685-1', 'María López', 'maria.lopez@inacapmail.cl', '+569738540000', date(2005, 1, 10), 20, 'F', 'CHILE', 2023, 500, 3),
    ]
    
    print(f"\n1. Insertando {len(estudiantes)} estudiantes...")
    
    for rut, nombre, email, tel, fecha_nac, edad, sexo, nac, ano_egreso, puntaje, familia in estudiantes:
        success, error = db.execute_query(
            "INSERT INTO Estudiante (rut, nombre, email_institucional, telefono, fecha_nacimiento, edad, sexo, nacionalidad, ano_egreso_media, puntaje_psu, integrantes_grupo_familiar) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (rut, nombre, email, tel, fecha_nac, edad, sexo, nac, ano_egreso, puntaje, familia)
        )
        status = "✓" if success else f"✗ {error[:40]}"
        print(f"   {status} {nombre}")
    
    # Verificar
    print("\n2. Verificando estudiantes insertados...")
    result = db.fetch_query("SELECT * FROM Estudiante")
    print(f"   Total de estudiantes: {len(result) if result else 0}")
    
    if result:
        for row in result:
            print(f"   - {row[2]} ({row[1]}) - Edad: {row[6]}")
    
    db.disconnect()


def ejemplo_6_consultas_practicas():
    """
    Ejemplo 6: Ejemplos de consultas prácticas
    """
    print("\n" + "="*60)
    print("EJEMPLO 6: Consultas prácticas útiles")
    print("="*60)
    
    db = DatabaseManager()
    db.connect()
    db.clear_tables()
    
    # Preparar datos
    db.execute_query("INSERT INTO Region (codigo, nombre) VALUES (%s, %s)", (11, 'Aysén'))
    db.execute_query("INSERT INTO Comuna (id_region, codigo, nombre) VALUES (%s, %s, %s)", (1, 1001, 'Coyhaique'))
    db.execute_query("INSERT INTO Colegio (id_comuna, id_region, rbd, nombre, tipo_colegio) VALUES (%s, %s, %s, %s, %s)", (1, 1, '24206-3', 'Colegio Alborada', 'PARTICULARES PAGADOS'))
    
    # Consulta 1: Contar registros
    print("\n1. Contar regiones:")
    result = db.fetch_query("SELECT COUNT(*) as cantidad FROM Region")
    print(f"   Cantidad: {result[0][0]}")
    
    # Consulta 2: Listar con JOIN
    print("\n2. Listar colegios con su región:")
    result = db.fetch_query("SELECT c.nombre, r.nombre FROM Colegio c JOIN Region r ON c.id_region = r.id_region")
    if result:
        for row in result:
            print(f"   - {row[0]} (Región: {row[1]})")
    
    # Consulta 3: Filtrar por condición
    print("\n3. Colegios de tipo PARTICULARES:")
    result = db.fetch_query("SELECT nombre, tipo_colegio FROM Colegio WHERE tipo_colegio LIKE '%PARTICULARES%'")
    if result:
        for row in result:
            print(f"   - {row[0]}: {row[1]}")
    
    db.disconnect()


if __name__ == "__main__":
    """
    Ejecutar ejemplos individuales descomenta la línea que quieras:
    """
    
    # ejemplo_1_insertar_datos_validos()
    # ejemplo_2_intentar_insertar_invalido()
    # ejemplo_3_cascade_eliminacion()
    # ejemplo_4_restrict_eliminacion()
    # ejemplo_5_insertar_multiples_estudiantes()
    # ejemplo_6_consultas_practicas()
    
    # Ejecutar todos:
    print("\n" + "🧪 EJEMPLOS DE TESTING - EJECUTANDO TODOS" + "\n")
    ejemplo_1_insertar_datos_validos()
    ejemplo_2_intentar_insertar_invalido()
    ejemplo_3_cascade_eliminacion()
    ejemplo_4_restrict_eliminacion()
    ejemplo_5_insertar_multiples_estudiantes()
    ejemplo_6_consultas_practicas()
    
    print("\n" + "="*60)
    print("✓ TODOS LOS EJEMPLOS COMPLETADOS")
    print("="*60 + "\n")
