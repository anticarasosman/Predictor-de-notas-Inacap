# Archivos que Requieren Migración

## ✅ Completados

### database/db_connection.py
- Estado: **MIGRADO COMPLETAMENTE**
- Usa: APIClient
- Métodos deprecados: cursor(), execute_query(), fetch_query()

### .env
- Estado: **ACTUALIZADO**
- Configuración: API_URL, API_TIMEOUT
- Variables MySQL removidas

### test_db_connection_api.py
- Estado: **CREADO Y VALIDADO**
- Propósito: Tests de DatabaseConnection con API
- Resultado: ✓ Todos los tests pasan

## ⬜ Pendientes de Migración

### 1. main.py (ALTA PRIORIDAD)
**Línea 6:** `from database.db_connection import DatabaseConnection`
**Línea 32:** `db_connection = DatabaseConnection()`

**Estado:** Usa DatabaseConnection pero probablemente solo para `connect()`
**Acción:** Verificar cómo usa la conexión

---

### 2. classes/readers/excel_reader/reporte_morosidad_reader.py
**Línea 23:** `cursor = self.db_connection.cursor()`

**Problema:** Usa cursor() directamente (ahora deprecado)
**Acción requerida:**
- Reemplazar cursor.execute() + cursor.fetchall() por métodos API
- Cambiar acceso de tuplas a diccionarios

---

### 3. utils/db_schema_reader.py
**Línea 25:** `tables = cursor.fetchall()`
**Línea 62:** `columns = cursor.fetchall()`

**Problema:** Lee esquema de base de datos directamente
**Opciones:**
1. Migrar a consulta_personalizada() si la tabla INFORMATION_SCHEMA está permitida
2. Crear endpoint Lambda específico para metadatos de esquema
3. Deprecar esta funcionalidad (probablemente no crítica para v3.0)

---

### 4. test_morosidad_reader.py (BAJA PRIORIDAD - TEST)
**Línea 11:** `from database.db_connection import DatabaseConnection`
**Múltiples líneas:** Usa cursor(), fetchone()

**Estado:** Archivo de testing, probablemente obsoleto
**Acción recomendada:** Eliminar (está en lista de archivos para borrar)

---

## 📋 Plan de Migración por Prioridad

### Prioridad 1: CRÍTICO (bloquea ejecución)
1. **main.py** - Archivo principal de la aplicación

### Prioridad 2: ALTA (funcionalidad core)
2. **reporte_morosidad_reader.py** - Reader usado por aplicación

### Prioridad 3: MEDIA (features secundarios)
3. **db_schema_reader.py** - Utilidad de metadatos (puede ser opcional)

### Prioridad 4: BAJA (testing/obsoletos)
4. **test_morosidad_reader.py** - Test obsoleto (candidato a eliminación)

## 🔍 Análisis Detallado Pendiente

### main.py
**Necesita revisión:**
```python
# Revisar si solo usa:
db_connection = DatabaseConnection()
db_connection.connect()
db_connection.is_connected()

# O si también ejecuta consultas:
db_connection.cursor()
db_connection.execute_query()
```

**Si solo usa connect/disconnect:** ✅ Ya funciona sin cambios
**Si usa cursor/queries:** ⚠️ Requiere migración

### reporte_morosidad_reader.py
**Patrón típico a cambiar:**
```python
# ANTES:
cursor = self.db_connection.cursor()
cursor.execute("SELECT * FROM estudiante WHERE rut = %s", (rut,))
resultado = cursor.fetchone()
if resultado:
    rut, nombre, email = resultado  # Tupla

# DESPUÉS:
try:
    estudiante = self.db_connection.buscar_estudiante(rut)
    if estudiante:
        rut = estudiante["rut"]      # Diccionario
        nombre = estudiante["nombre"]
        email = estudiante["email"]
except APIClientError as e:
    # Manejo de error
```

## 🎯 Próximo Paso Recomendado

**OPCIÓN A - Análisis Profundo:**
1. Leer main.py completo
2. Leer reporte_morosidad_reader.py completo
3. Identificar todos los usos de cursor/execute/fetch
4. Crear plan de migración específico por archivo

**OPCIÓN B - Prueba y Error:**
1. Intentar ejecutar main.py con db_connection migrado
2. Ver qué errores aparecen
3. Corregir uno por uno basado en errores reales

**OPCIÓN C - Migración Incremental:**
1. Migrar main.py primero (crítico)
2. Testear que arranca la aplicación
3. Migrar reporte_morosidad_reader.py
4. Testear funcionalidad completa

## ✅ Recomendación

**Empezar con OPCIÓN A + OPCIÓN C combinadas:**
1. Leer y analizar main.py (5 minutos)
2. Migrar main.py si necesario (10 minutos)
3. Testear arranque de aplicación (5 minutos)
4. Continuar con readers según necesidad

**Ventaja:** Validación temprana de la arquitectura
**Riesgo:** Bajo (main.py probablemente solo usa connect())
