# 🚀 Guía Rápida: Testing con Datos Semilla

## ✅ ¿Qué cambió?

Ahora **todos tus tests tienen datos precargados automáticamente**. Ya no necesitas insertar Region, Comuna, Estudiante, etc. manualmente en cada test.

## 📊 Datos Disponibles

### 🎓 **8 Estudiantes**
| RUT | Nombre | Carrera | Email |
|-----|--------|---------|-------|
| `20587683-9` | Camila Manríquez | Administración | camila.manriquez07@inacapmail.cl |
| `21195581-3` | Anahí Formantel | Odontología | anahi.formantel@inacapmail.cl |
| `21379413-2` | Dante Agüero | Analista Programador | dante.aguero@inacapmail.cl |
| ... | +5 estudiantes más | ... | ... |

### 🏫 **4 Regiones, 6 Comunas, 4 Colegios**
### 📚 **10 Ramos, 3 Carreras, 9 Profesores**
### 💰 **Pagos, Cuotas, Inscripciones, etc.**

Ver [database/seed_data/README.md](../database/seed_data/README.md) para lista completa.

---

## 🎯 Ejemplos de Uso

### ❌ ANTES (complicado)
```python
def test_notas_estudiante(self, db):
    # Insertar región
    db.execute_query("INSERT INTO Region (codigo, nombre) VALUES (%s, %s)", (11, 'Aysén'))
    # Insertar comuna
    db.execute_query("INSERT INTO Comuna (id_region, codigo, nombre) VALUES (%s, %s, %s)", (1, 1001, 'Coyhaique'))
    # Insertar estudiante
    db.execute_query("INSERT INTO Estudiante (rut, nombre, email_institucional, ...) VALUES (...)", (...))
    # ... 20 líneas más de inserciones ...
    
    # Finalmente el test real
    result = db.fetch_query("SELECT promedio FROM Notas WHERE id_estudiante = 1")
    assert result[0][0] > 4.0
```

### ✅ AHORA (simple)
```python
def test_notas_estudiante(self, db):
    # ¡Camila ya existe con rut 20587683-9!
    result = db.fetch_query(
        "SELECT id_estudiante FROM Estudiante WHERE rut = %s",
        ('20587683-9',)
    )
    est_id = result[0][0]
    
    # Tu test real
    result = db.fetch_query("SELECT promedio_matematicas FROM Notas_Estudiante WHERE id_estudiante = %s", (est_id,))
    assert result[0][0] == 4.1  # Camila tiene promedio 4.1
```

---

## 💡 Tips y Trucos

### 1️⃣ **Usar RUT en lugar de ID**
```python
# ✅ MEJOR: Usa RUT (más estable)
result = db.fetch_query("SELECT * FROM Estudiante WHERE rut = %s", ('20587683-9',))

# ❌ EVITAR: IDs pueden cambiar
result = db.fetch_query("SELECT * FROM Estudiante WHERE id_estudiante = 1")
```

### 2️⃣ **Verificar datos semilla primero**
```python
def test_mi_funcionalidad(self, db):
    # Verificar que el dato existe
    result = db.fetch_query("SELECT id FROM Carrera WHERE codigo_carrera = %s", ('AE',))
    assert result, "Carrera AE no está en datos semilla"
    
    carrera_id = result[0][0]
    # Continuar con el test...
```

### 3️⃣ **Datos útiles para tests comunes**

#### Test de Notas:
```python
# Anahí tiene promedio 5.5 en matemáticas
result = db.fetch_query(
    "SELECT promedio_matematicas FROM Notas_Estudiante WHERE id_estudiante = (SELECT id_estudiante FROM Estudiante WHERE rut = %s)",
    ('21195581-3',)
)
assert result[0][0] == 5.5
```

#### Test de Pagos/Deudas:
```python
# Camila tiene deuda
result = db.fetch_query(
    "SELECT COUNT(*) FROM Pagos WHERE estado_pago = 'VENCIDO' AND id_matricula IN (SELECT id_matricula FROM Matricula WHERE id_estudiante = (SELECT id_estudiante FROM Estudiante WHERE rut = %s))",
    ('20587683-9',)
)
assert result[0][0] > 0  # Tiene deuda
```

#### Test de Inscripciones:
```python
# Anahí está inscrita en Inglés II
result = db.fetch_query("""
    SELECT nota_final FROM Inscripciones_Ramos 
    WHERE id_estudiante = (SELECT id_estudiante FROM Estudiante WHERE rut = %s)
""", ('21195581-3',))
assert result[0][0] == 6.60
```

---

## 🔧 Fixture Options

### Opción 1: Con datos semilla (por defecto)
```python
def test_con_datos(self, db):
    # db ya tiene 8 estudiantes, 4 regiones, etc.
    result = db.fetch_query("SELECT COUNT(*) FROM Estudiante")
    assert result[0][0] >= 8
```

### Opción 2: BD completamente vacía
```python
def test_desde_cero(self, db_empty):
    # db_empty NO tiene datos precargados
    result = db_empty.fetch_query("SELECT COUNT(*) FROM Estudiante")
    assert result[0][0] == 0
    
    # Insertar tus propios datos...
```

---

## 🐛 Troubleshooting

### Problema: "No encuentro el estudiante X"
**Solución**: Revisa [database/seed_data/10_estudiante.sql](../database/seed_data/10_estudiante.sql) para ver qué estudiantes están disponibles.

### Problema: "IDs no coinciden"
**Solución**: No uses IDs directamente. Usa RUT, código_carrera, sigla de ramo, etc.

### Problema: "Necesito más datos"
**Solución**: Agrega más datos a los archivos .sql en `database/seed_data/` y recarga:
```python
db.load_seed_data()
```

### Problema: "Quiero BD vacía para un test específico"
**Solución**: Usa fixture `db_empty` en lugar de `db`:
```python
def test_mi_caso_especial(self, db_empty):
    # Empieza desde cero
```

---

## 📈 Beneficios

✅ **Tests más rápidos**: No insertas 50 líneas de datos cada vez  
✅ **Más fácil de leer**: Tests se enfocan en lo que prueban  
✅ **Consistente**: Todos usan los mismos datos base  
✅ **Realista**: Datos basados en CSV reales de INACAP  

---

## 🔗 Recursos

- [README de Seed Data](../database/seed_data/README.md) - Lista completa de datos
- [conftest.py](conftest.py) - Configuración de fixtures
- [Ejemplos](ejemplos_testing.py) - Más ejemplos de uso

---

**¿Preguntas?** Revisa los archivos en `database/seed_data/` para ver exactamente qué datos tienes disponibles.
