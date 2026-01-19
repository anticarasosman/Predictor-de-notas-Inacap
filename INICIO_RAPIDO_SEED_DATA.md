# 🎯 INICIO RÁPIDO: Sistema de Datos Semilla

## ✅ ¿Qué se implementó?

Tu base de datos ahora tiene **datos semilla automáticos** que se cargan cada vez que ejecutas un test. Ya no necesitas insertar manualmente Region, Comuna, Estudiante, etc.

---

## 🚀 PASO 1: Verificar que Funciona

Abre tu terminal de PowerShell en el proyecto y ejecuta:

```powershell
# Activar entorno virtual (si no está activo)
.\.venv\Scripts\Activate.ps1

# Ejecutar test de verificación
pytest testing/test_verificar_seed_data.py -v
```

### ✅ Si ves esto, ¡funciona perfecto!
```
test_regiones_cargadas PASSED ✓
test_estudiantes_cargados PASSED ✓
test_carreras_cargadas PASSED ✓
...
```

### ❌ Si ves errores:
1. Verifica que tu BD `inacap_test` existe y está accesible
2. Revisa el archivo [database/PROBLEMAS_SCHEMAS.md](database/PROBLEMAS_SCHEMAS.md) para correcciones necesarias
3. Las tablas deben existir antes de cargar datos

---

## 📖 PASO 2: Ver Qué Datos Tienes

Consulta la guía completa de datos disponibles:
- [testing/GUIA_DATOS_SEMILLA.md](testing/GUIA_DATOS_SEMILLA.md) - Guía rápida con ejemplos
- [database/seed_data/README.md](database/seed_data/README.md) - Lista completa de datos

### Resumen rápido:
- **8 Estudiantes** (incluyendo Camila Manríquez, Anahí Formantel, Dante Agüero)
- **4 Regiones** (Aysén, Metropolitana, Valparaíso, Biobío)
- **10 Ramos** (Matemáticas, Inglés, Lenguaje, técnicos)
- **3 Carreras** (Administración, Odontología, Analista Programador)
- **9 Profesores**
- Y mucho más...

---

## 💡 PASO 3: Escribir Tests Rápido

### Ejemplo: Test de Notas

**ANTES (complicado):**
```python
def test_notas(self, db):
    # 30+ líneas insertando Region, Comuna, Estudiante...
    db.execute_query("INSERT INTO Region...")
    db.execute_query("INSERT INTO Comuna...")
    db.execute_query("INSERT INTO Estudiante...")
    # ...
```

**AHORA (simple):**
```python
def test_notas(self, db):
    # ¡Camila ya existe!
    result = db.fetch_query(
        "SELECT promedio_matematicas FROM Notas_Estudiante WHERE id_estudiante = (SELECT id_estudiante FROM Estudiante WHERE rut = %s)",
        ('20587683-9',)
    )
    assert result[0][0] == 4.1
```

### Ejemplo: Test de Relaciones

```python
def test_estudiante_con_colegio(self, db):
    # Camila ya está relacionada con COLEGIO TRAPANANDA
    result = db.fetch_query("""
        SELECT c.nombre 
        FROM Colegio c
        JOIN estudiante_colegio ec ON c.id_colegio = ec.id_colegio
        JOIN Estudiante e ON ec.id_estudiante = e.id_estudiante
        WHERE e.rut = %s
    """, ('20587683-9',))
    
    assert result[0][0] == 'COLEGIO TRAPANANDA'
```

---

## 🔧 PASO 4: Ejecutar Tus Tests Actualizados

```powershell
# Tests de inserciones válidas
pytest testing/tests_de_inserciones_validas/ -v

# Tests de inserciones inválidas
pytest testing/tests_de_inserciones_invalidas/ -v

# Tests de CASCADE y RESTRICT
pytest testing/tests_de_cascade_y_restrict/ -v

# Ejecutar TODO
pytest testing/ -v
```

---

## 🎓 Tips Importantes

### 1️⃣ Usa RUT, no IDs
```python
# ✅ CORRECTO: Más estable
result = db.fetch_query("SELECT * FROM Estudiante WHERE rut = %s", ('20587683-9',))

# ❌ EVITAR: IDs pueden cambiar
result = db.fetch_query("SELECT * FROM Estudiante WHERE id_estudiante = 1")
```

### 2️⃣ Fixture: `db` vs `db_empty`
```python
# Con datos precargados (por defecto)
def test_con_datos(self, db):
    # 8 estudiantes ya existen
    pass

# BD completamente vacía
def test_desde_cero(self, db_empty):
    # 0 estudiantes
    pass
```

### 3️⃣ Estudiantes útiles para tests

| RUT | Nombre | Tiene Notas | Tiene Deuda | Carrera |
|-----|--------|-------------|-------------|---------|
| 20587683-9 | Camila | ✅ Sí | ✅ Sí | Administración |
| 21195581-3 | Anahí | ✅ Sí | ❌ No | Odontología |
| 21379413-2 | Dante | ✅ Sí | ❌ No | Analista Prog. |

---

## 📂 Estructura de Archivos

```
database/
  seed_data/
    01_region.sql ← Datos de regiones
    02_area_academica.sql
    ...
    27_ramosPlanEstudio_prerequisito.sql
    master_seed.sql ← Script maestro
    README.md ← Documentación completa

testing/
  conftest.py ← Configuración actualizada
  GUIA_DATOS_SEMILLA.md ← Guía rápida
  test_verificar_seed_data.py ← Test de verificación
  tests_de_inserciones_validas/ ← Tests actualizados
  tests_de_inserciones_invalidas/ ← Tests actualizados
  tests_de_cascade_y_restrict/ ← Tests actualizados
```

---

## 🆘 Solución de Problemas

### Problema: "No se cargan los datos"
```python
# Cargar manualmente
db.load_seed_data()
```

### Problema: "Estudiante X no existe"
Revisa [database/seed_data/10_estudiante.sql](database/seed_data/10_estudiante.sql) para ver qué estudiantes están disponibles.

### Problema: "Error de sintaxis en SQL"
Revisa [database/PROBLEMAS_SCHEMAS.md](database/PROBLEMAS_SCHEMAS.md) para correcciones necesarias.

### Problema: "Quiero agregar más datos"
1. Edita el archivo .sql correspondiente en `database/seed_data/`
2. Ejecuta: `db.load_seed_data()` o recarga con `master_seed.sql`

---

## ✨ Siguiente Nivel

Una vez que domines los datos semilla:

1. **Agrega más estudiantes**: Edita `database/seed_data/10_estudiante.sql`
2. **Agrega más ramos**: Edita `database/seed_data/07_ramo.sql`
3. **Crea casos de prueba específicos**: Agrega datos que representen casos edge
4. **Automatiza más**: Integra con CI/CD

---

## 📞 Recursos

- **Guía Rápida**: [testing/GUIA_DATOS_SEMILLA.md](testing/GUIA_DATOS_SEMILLA.md)
- **Datos Completos**: [database/seed_data/README.md](database/seed_data/README.md)
- **Implementación**: [IMPLEMENTACION_SEED_DATA.md](IMPLEMENTACION_SEED_DATA.md)
- **Problemas Conocidos**: [database/PROBLEMAS_SCHEMAS.md](database/PROBLEMAS_SCHEMAS.md)

---

## 🎉 ¡Comienza Ahora!

```powershell
# Verifica que funciona
pytest testing/test_verificar_seed_data.py -v

# Ejecuta un test actualizado
pytest testing/tests_de_inserciones_validas/test_validas.py::TestInsertarDatosValidos::test_verificar_datos_semilla_cargados -v

# ¡Y ya puedes escribir tests más rápido! 🚀
```

---

**Fecha**: Enero 19, 2026  
**Estado**: ✅ Listo para usar  
**Base de datos**: `inacap_test`
