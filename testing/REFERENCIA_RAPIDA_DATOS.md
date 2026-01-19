# 📋 Referencia Rápida: Datos Semilla

## 🎓 Estudiantes (usar por RUT)

```python
# Estudiante 1: Camila Manríquez
rut = '20587683-9'
# - Carrera: Administración de Empresas
# - Tiene deuda: SÍ
# - Tiene notas: SÍ (Mat: 4.1, Leng: 4.7, Ing: 4.6)
# - Tiene historial: SÍ

# Estudiante 2: Tammy Adriazola
rut = '20967147-6'
# - Carrera: Administración de Empresas
# - Tiene deuda: SÍ

# Estudiante 3: María Valencia
rut = '21265811-1'
# - Carrera: Administración de Empresas

# Estudiante 4: Anahí Formantel
rut = '21195581-3'
# - Carrera: Técnico en Odontología
# - Tiene notas: SÍ (Mat: 5.5, Leng: 6.0, Ing: 6.8)
# - Inscrita en: Inglés II (nota final: 6.60)
# - Tiene historial: SÍ

# Estudiante 5: Javiera Mansilla
rut = '21376766-6'
# - Carrera: Técnico en Odontología
# - Inscrita en: Inglés II (nota final: 6.90)

# Estudiante 6: Natalia Ojeda
rut = '21479949-9'
# - Carrera: Técnico en Odontología
# - Inscrita en: Inglés II (nota final: 6.60)

# Estudiante 7: Dante Agüero
rut = '21379413-2'
# - Carrera: Analista Programador
# - Tiene notas: SÍ (Mat: 6.5, Leng: 6.3, Ing: 6.8)

# Estudiante 8: Andrea Belmar
rut = '19817058-5'
# - Carrera: Administración de Empresas
# - Es trabajador: SÍ
```

## 🏫 Regiones (usar por código)

```python
region_aysen = 11  # 'Aysén del General Carlos Ibáñez del Campo'
region_metropolitana = 13  # 'Región Metropolitana'
region_valparaiso = 5  # 'Valparaíso'
region_biobio = 8  # 'Biobío'
```

## 🏘️ Comunas (usar por nombre)

```python
# En Aysén:
'Coyhaique'
'Puerto Aysén'

# En Metropolitana:
'Santiago'
'Providencia'

# En Valparaíso:
'Valparaíso'
'Viña del Mar'
```

## 🏢 Colegios (usar por RBD o nombre)

```python
# RBD '24206-3': COLEGIO TRAPANANDA
# RBD '24207-1': LICEO JOSEFINA AGUIRRE MONTENEGRO
# RBD '24208-K': COLEGIO KALEM
# RBD '24209-8': CIPRESES
```

## 📚 Carreras (usar por código)

```python
carrera_administracion = 'AE'  # Administración de Empresas
carrera_odontologia = 'OD'     # Técnico en Odontología
carrera_programador = 'B5'     # Analista Programador
```

## 📖 Ramos (usar por sigla)

```python
# Matemáticas
'MAT101'  # Matemática I
'MAT102'  # Matemática II
'MAT201'  # Cálculo I

# Inglés
'IDEN01'  # Inglés I
'IDEN02'  # Inglés II
'IDEN03'  # Inglés III

# Lenguaje
'LEN101'  # Comunicación Efectiva
'LEN102'  # Taller de Escritura

# Técnicos
'TEC101'  # Introducción a la Programación
'SAL101'  # Anatomía Básica
```

## 👨‍🏫 Profesores (usar por RUT)

```python
# Matemáticas
'12345678-9'  # Rojas Silva Pedro Eladio
'12345679-7'  # Carrasco Soto Cristhian Arcadio
'12345680-0'  # Barros Rojas Rosalba Margot

# Inglés
'12345681-9'  # Maldonado Almonacid Diandra Alejandra
'12345682-7'  # Zúñiga Vera Yinnia Valeska
'12345683-5'  # Molina Garrido Ricardo Andres

# Comunicación
'12345684-3'  # Gonzalez Frychel Claudia Andrea
'12345685-1'  # Fontecha Bórquez Tatiana Lorena
'12345686-K'  # Inzulza Reyes Marcelo Osvaldo Antonio
```

## 💰 Estados de Pago

```python
# Estudiantes CON deuda:
'20587683-9'  # Camila - Matrícula + Arancel vencidos
'20967147-6'  # Tammy - Matrícula vencida

# Estudiantes SIN deuda:
'21195581-3'  # Anahí - Matrícula pagada
```

## 🎯 Consultas Comunes

### Obtener ID de estudiante por RUT
```python
result = db.fetch_query(
    "SELECT id_estudiante FROM Estudiante WHERE rut = %s",
    ('20587683-9',)
)
id_est = result[0][0]
```

### Obtener ID de carrera por código
```python
result = db.fetch_query(
    "SELECT id_carrera FROM Carrera WHERE codigo_carrera = %s",
    ('AE',)
)
id_carrera = result[0][0]
```

### Obtener promedio de estudiante
```python
result = db.fetch_query("""
    SELECT promedio_matematicas, promedio_lenguaje, promedio_ingles
    FROM Notas_Estudiante 
    WHERE id_estudiante = (SELECT id_estudiante FROM Estudiante WHERE rut = %s)
""", ('21195581-3',))
mat, leng, ing = result[0]
```

### Verificar si tiene deuda
```python
result = db.fetch_query("""
    SELECT COUNT(*) FROM Pagos p
    JOIN Matricula m ON p.id_matricula = m.id_matricula
    WHERE m.id_estudiante = (SELECT id_estudiante FROM Estudiante WHERE rut = %s)
    AND p.estado_pago = 'VENCIDO'
""", ('20587683-9',))
tiene_deuda = result[0][0] > 0
```

### Obtener inscripciones de estudiante
```python
result = db.fetch_query("""
    SELECT r.nombre_ramo, i.nota_final, i.situacion_final
    FROM Inscripciones_Ramos i
    JOIN Secciones_Ramos s ON i.id_seccion = s.id_seccion_ramo
    JOIN Ramo r ON s.id_ramo = r.id_ramo
    WHERE i.id_estudiante = (SELECT id_estudiante FROM Estudiante WHERE rut = %s)
""", ('21195581-3',))
```

---

## 📌 Tips de Uso

1. **Siempre usa RUT, códigos o siglas** en lugar de IDs autoincrementales
2. **Verifica primero que el dato existe** con un SELECT antes de usarlo
3. **Usa JOINs** para relacionar datos en lugar de múltiples queries
4. **Consulta los archivos .sql** si necesitas ver los datos exactos

---

**Archivo de referencia rápida para copiar y pegar en tus tests**
