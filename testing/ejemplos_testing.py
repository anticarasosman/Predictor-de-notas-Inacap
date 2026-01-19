"""
=============================================================================
GUÍA DE TESTING CON PYTEST - Base de Datos Inacap
=============================================================================

⚠️ IMPORTANTE: ESTE ARCHIVO ES SOLO DOCUMENTACIÓN / GUÍA DE REFERENCIA
    NO ESTÁ DISEÑADO PARA SER EJECUTADO COMO TESTS.
    
    Los tests reales están en: testing/test_database.py

CARACTERÍSTICAS PRINCIPALES:
- Uso de fixtures automáticos (db, db_empty)
- Seed data precargado en cada test
- Pytest markers para organizar tests
- Integración con VS Code Test Explorer

COMANDOS ÚTILES:
----------------
# Ejecutar todos los tests REALES
pytest testing/test_database.py -v

# Ejecutar solo tests marcados como "valid"
pytest testing/test_database.py -m valid -v

# Ejecutar solo tests marcados como "invalid"
pytest testing/test_database.py -m invalid -v

# Ejecutar tests de constraints (CASCADE/RESTRICT)
pytest testing/test_database.py -m constraints -v

# Ejecutar tests que verifican seed data
pytest testing/test_database.py -m seed -v

MARKERS DISPONIBLES:
-------------------
@pytest.mark.valid       - Tests de inserciones válidas
@pytest.mark.invalid     - Tests de inserciones inválidas/duplicados
@pytest.mark.constraints - Tests de CASCADE/RESTRICT
@pytest.mark.seed        - Tests que verifican datos semilla
@pytest.mark.slow        - Tests que tardan más tiempo

=============================================================================
"""

# NOTA: Los siguientes son ejemplos de CÓMO escribir tests.
# Para ejecutar tests reales, usa: testing/test_database.py


# =============================================================================
# SECCIÓN 1: Tests Básicos con Seed Data
# =============================================================================

"""
EJEMPLO 1: Verificar que los datos semilla están disponibles

La fixture 'db' automáticamente:
1. Limpia todas las tablas
2. Carga los datos semilla
3. Los pone disponibles para el test

Código de ejemplo:
"""

# @pytest.mark.seed
# def test_verificar_seed_data_disponible(db):
#     # Verificar regiones
#     result = db.fetch_query("SELECT COUNT(*) FROM Region")
#     assert result[0][0] >= 4, "Datos semilla de regiones no cargados"
#     
#     # Verificar estudiantes
#     result = db.fetch_query("SELECT COUNT(*) FROM Estudiante")
#     assert result[0][0] >= 8, "Datos semilla de estudiantes no cargados"


"""
EJEMPLO 2: Insertar datos nuevos además del seed

Los datos semilla ya están cargados, puedes agregar más datos sin problema.

Código de ejemplo:
"""

# @pytest.mark.valid
# def test_insertar_dato_nuevo(db):
#     # El seed ya tiene regiones, agregamos una nueva
#     query = "INSERT INTO Region (codigo, nombre) VALUES (%s, %s)"
#     success, error = db.execute_query(query, (10, 'Región Nueva'))
#     
#     assert success, f"Error al insertar: {error}"
#     
#     # Verificar que se insertó
#     result = db.fetch_query("SELECT nombre FROM Region WHERE codigo = %s", (10,))
#     assert result[0][0] == 'Región Nueva'


# =============================================================================
# SECCIÓN 2: Tests de Validación (Datos Inválidos)
# =============================================================================

"""
EJEMPLO 3: Verificar que restricciones UNIQUE funcionan

El seed ya tiene la región con código 11, intentar duplicarla debe fallar.

Código de ejemplo:
"""

# @pytest.mark.invalid
# def test_no_permitir_codigo_region_duplicado(db):
#     query = "INSERT INTO Region (codigo, nombre) VALUES (%s, %s)"
#     success, _ = db.execute_query(query, (11, 'Duplicado'))
#     
#     # Debe fallar
#     assert not success, "Se permitió insertar código duplicado"


"""
EJEMPLO 4: Verificar que restricciones FOREIGN KEY funcionan

Intentar insertar comuna con región inexistente debe fallar.

Código de ejemplo:
"""

# @pytest.mark.invalid
# def test_no_permitir_foreign_key_invalido(db):
#     query = "INSERT INTO Comuna (id_region, codigo, nombre) VALUES (%s, %s, %s)"
#     success, error = db.execute_query(query, (99999, 1001, 'Comuna Inválida'))
#     
#     # Debe fallar
#     assert not success, "Se permitió insertar FK inválida"
#     assert error and ("FOREIGN KEY" in error or "foreign key" in error.lower())


"""
EJEMPLO 5: Verificar unicidad de emails

El seed tiene el email 'camila.manriquez07@inacapmail.cl',
intentar usarlo de nuevo debe fallar.

Código de ejemplo:
"""

# from datetime import date
# 
# @pytest.mark.invalid
# def test_no_permitir_email_duplicado(db):
#     query = (
#         "INSERT INTO Estudiante "
#         "(rut, nombre, email_institucional, telefono, fecha_nacimiento, edad, "
#         "sexo, nacionalidad, ano_egreso_media, puntaje_psu, integrantes_grupo_familiar) "
#         "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
#     )
#     
#     success, _ = db.execute_query(
#         query,
#         (
#             '99999999-9',
#             'Estudiante Duplicado',
#             'camila.manriquez07@inacapmail.cl',  # Email que ya existe en seed
#             '+569999999',
#             date(2005, 1, 1),
#             20,
#             'M',
#             'CHILE',
#             2022,
#             600,
#             4,
#         ),
#     )
#     
#     assert not success, "Se permitió insertar email duplicado"


# =============================================================================
# SECCIÓN 3: Tests de Relaciones (CASCADE y RESTRICT)
# =============================================================================

"""
EJEMPLO 6: Verificar comportamiento ON DELETE CASCADE

Al eliminar un estudiante, su historial institucional
debe eliminarse automáticamente.

Código de ejemplo:
"""

# @pytest.mark.constraints
# def test_cascade_eliminar_estudiante_elimina_historial(db):
#     # Buscar estudiante del seed (Camila)
#     row = db.fetch_query("SELECT id_estudiante FROM Estudiante WHERE rut = %s", ('20587683-9',))
#     assert row and row[0], "Estudiante Camila no encontrada en seed"
#     est_id = row[0][0]
#     
#     # Verificar que tiene historial
#     result = db.fetch_query(
#         "SELECT COUNT(*) FROM HistorialInstitucional WHERE id_estudiante = %s",
#         (est_id,)
#     )
#     count_antes = result[0][0]
#     assert count_antes > 0, "El estudiante no tiene historial en seed"
#     
#     # Eliminar estudiante
#     success, _ = db.execute_query("DELETE FROM Estudiante WHERE id_estudiante = %s", (est_id,))
#     assert success, "No se pudo eliminar el estudiante"
#     
#     # Verificar que su historial también se eliminó (CASCADE)
#     result = db.fetch_query(
#         "SELECT COUNT(*) FROM HistorialInstitucional WHERE id_estudiante = %s",
#         (est_id,)
#     )
#     count_despues = result[0][0]
#     assert count_despues == 0, "El historial no se eliminó por CASCADE"


"""
EJEMPLO 7: Verificar comportamiento ON DELETE RESTRICT

No se debe poder eliminar un colegio que tiene estudiantes asociados.

Código de ejemplo:
"""

# @pytest.mark.constraints
# def test_restrict_no_eliminar_colegio_con_estudiantes(db):
#     # Buscar colegio del seed que tiene estudiantes
#     row = db.fetch_query("SELECT id_colegio FROM Colegio WHERE rbd = %s", ('24206-3',))
#     assert row and row[0], "Colegio no encontrado en seed"
#     id_colegio = row[0][0]
#     
#     # Verificar que tiene estudiantes
#     result = db.fetch_query(
#         "SELECT COUNT(*) FROM Estudiante_Colegio WHERE id_colegio = %s",
#         (id_colegio,)
#     )
#     if result[0][0] == 0:
#         pytest.skip("El colegio no tiene estudiantes en seed")
#     
#     # Intentar eliminar (debe fallar por RESTRICT)
#     success, error = db.execute_query("DELETE FROM Colegio WHERE id_colegio = %s", (id_colegio,))
#     
#     # Verificar que no se permitió
#     assert not success, "Se permitió eliminar colegio con estudiantes"
#     assert error and ("FOREIGN KEY" in error or "restrict" in error.lower())


"""
EJEMPLO 8: CASCADE en relaciones jerárquicas

Al eliminar una región, todas sus comunas deben eliminarse.

Código de ejemplo:
"""

# @pytest.mark.constraints
# def test_cascade_eliminar_region_elimina_comunas(db):
#     # Buscar región del seed (Aysén - código 11)
#     row = db.fetch_query("SELECT id_region FROM Region WHERE codigo = %s", (11,))
#     assert row and row[0], "Región Aysén no encontrada en seed"
#     id_region = row[0][0]
#     
#     # Contar comunas antes
#     result = db.fetch_query("SELECT COUNT(*) FROM Comuna WHERE id_region = %s", (id_region,))
#     count_antes = result[0][0]
#     assert count_antes > 0, "La región no tiene comunas en seed"
#     
#     # Eliminar región
#     success, _ = db.execute_query("DELETE FROM Region WHERE id_region = %s", (id_region,))
#     assert success, "No se pudo eliminar la región"
#     
#     # Verificar que las comunas se eliminaron
#     result = db.fetch_query("SELECT COUNT(*) FROM Comuna WHERE id_region = %s", (id_region,))
#     count_despues = result[0][0]
#     assert count_despues == 0, "Las comunas no se eliminaron por CASCADE"


# =============================================================================
# SECCIÓN 4: Tests con Datos Relacionados
# =============================================================================

"""
EJEMPLO 9: Trabajar con foreign keys existentes del seed

Usar IDs de registros del seed para crear nuevas relaciones.

Código de ejemplo:
"""

# @pytest.mark.valid
# def test_insertar_con_relaciones(db):
#     # Buscar región del seed
#     row = db.fetch_query("SELECT id_region FROM Region WHERE codigo = %s", (11,))
#     assert row and row[0], "Región no encontrada"
#     id_region = row[0][0]
#     
#     # Crear nueva comuna relacionada
#     query = "INSERT INTO Comuna (id_region, codigo, nombre) VALUES (%s, %s, %s)"
#     success, error = db.execute_query(query, (id_region, 88888, 'Comuna Nueva'))
#     assert success, f"Error al crear comuna: {error}"
#     
#     # Verificar que se creó con la relación correcta
#     result = db.fetch_query(
#         "SELECT c.nombre, r.nombre FROM Comuna c "
#         "JOIN Region r ON c.id_region = r.id_region "
#         "WHERE c.codigo = %s",
#         (88888,)
#     )
#     assert result[0][0] == 'Comuna Nueva'
#     assert result[0][1] == 'Aysén del General Carlos Ibáñez del Campo'


"""
EJEMPLO 10: Consultas complejas con JOINs usando seed data

Verificar que las relaciones del seed están bien formadas.

Código de ejemplo:
"""

# @pytest.mark.seed
# def test_consulta_con_joins(db):
#     query = \"\"\"
#         SELECT e.nombre, c.nombre, r.nombre
#         FROM Estudiante e
#         LEFT JOIN Comuna c ON e.id_comuna_actual = c.id_comuna
#         LEFT JOIN Region r ON e.id_region_procedencia = r.id_region
#         WHERE e.rut = %s
#     \"\"\"
#     
#     result = db.fetch_query(query, ('20587683-9',))  # Camila del seed
#     assert result and result[0], "Estudiante no encontrado"
#     
#     nombre, comuna, region = result[0]
#     assert 'Camila' in nombre


# =============================================================================
# SECCIÓN 5: Uso de Fixture db_empty (sin seed data)
# =============================================================================

"""
EJEMPLO 11: Usar fixture db_empty para tests desde cero

A veces necesitas una BD completamente vacía sin datos semilla.
Usa la fixture 'db_empty' en lugar de 'db'.

Código de ejemplo:
"""

# @pytest.mark.valid
# def test_con_base_vacia(db_empty):
#     # Verificar que está vacía
#     result = db_empty.fetch_query("SELECT COUNT(*) FROM Region")
#     assert result[0][0] == 0, "La BD no está vacía"
#     
#     # Insertar desde cero
#     query = "INSERT INTO Region (codigo, nombre) VALUES (%s, %s)"
#     success, _ = db_empty.execute_query(query, (1, 'Primera Región'))
#     assert success
#     
#     result = db_empty.fetch_query("SELECT COUNT(*) FROM Region")
#     assert result[0][0] == 1, "No se insertó correctamente"


# =============================================================================
# INTEGRACIÓN CON VS CODE
# =============================================================================

"""
=========================================================================
CÓMO USAR ESTOS TESTS EN VS CODE
=========================================================================

1. INSTALAR EXTENSIÓN DE PYTHON:
   - Busca "Python" en extensiones de VS Code
   - Instala la extensión oficial de Microsoft

2. ACTIVAR TEST EXPLORER:
   - Presiona Ctrl+Shift+P
   - Busca "Python: Configure Tests"
   - Selecciona "pytest"
   - Selecciona el directorio "testing"

3. VER TESTS EN LA INTERFAZ:
   - Icono de matraz en la barra lateral izquierda
   - Verás todos los tests organizados por archivo
   - Los markers aparecerán como etiquetas

4. EJECUTAR TESTS:
   - Click derecho en un test → "Run Test"
   - Click en el botón de play junto a cada test
   - Click en "Run All Tests" para ejecutar todos

5. FILTRAR POR MARKERS:
   - En terminal: pytest testing/test_database.py -m valid
   - En terminal: pytest testing/test_database.py -m constraints
   - En terminal: pytest testing/test_database.py -m seed

6. DEBUGGING:
   - Click derecho en un test → "Debug Test"
   - Agrega breakpoints en el código
   - Inspecciona variables durante la ejecución

=========================================================================
COMANDOS RÁPIDOS DE TERMINAL
=========================================================================

# Ejecutar todos los tests con output detallado
python -m pytest testing/test_database.py -v

# Ejecutar solo tests marcados como "valid"
python -m pytest testing/test_database.py -m valid -v

# Ejecutar solo tests marcados como "invalid"
python -m pytest testing/test_database.py -m invalid -v

# Ver todos los markers disponibles
python -m pytest testing/test_database.py --markers

# Ejecutar con output más detallado
python -m pytest testing/test_database.py -vv

# Ejecutar y mostrar prints
python -m pytest testing/test_database.py -v -s

=========================================================================
"""
