# 🌱 Datos Semilla (Seed Data) para Testing

Este directorio contiene datos iniciales para todas las tablas de la base de datos `inacap_test`, facilitando el testing sin necesidad de insertar datos manualmente cada vez.

## 📁 Estructura de Archivos

Los archivos están numerados en orden de dependencias para garantizar una carga correcta:

### Fase 1: Tablas Base (01-04)
- `01_region.sql` - Regiones de Chile
- `02_area_academica.sql` - Áreas académicas de INACAP
- `03_area_conocimiento.sql` - Áreas de conocimiento para ramos
- `04_institucion.sql` - CFT e IP

### Fase 2: Tablas con 1 Dependencia (05-08)
- `05_comuna.sql` - Comunas por región
- `06_direccion.sql` - Direcciones de ejemplo
- `07_ramo.sql` - Ramos académicos
- `08_profesor.sql` - Profesores

### Fase 3: Dependencias Compuestas (09-16)
- `09_colegio.sql` - Colegios de egreso
- `10_estudiante.sql` - 8 estudiantes de ejemplo (basados en CSV reales)
- `11_plan_estudio.sql` - Planes de estudio vigentes
- `12_carrera.sql` - Carreras disponibles
- `13_historial_institucional.sql` - Historial previo de estudiantes
- `14_prerequisitos.sql` - Prerequisitos de ramos
- `15_ramos_plan_estudio.sql` - Ramos en planes de estudio
- `16_secciones_ramos.sql` - Secciones disponibles

### Fase 4: Gestión Académica (17-23)
- `17_predictor_datos.sql` - Datos del predictor de progresión
- `18_matricula.sql` - Matrículas activas
- `19_notas_estudiante.sql` - Promedios de notas
- `20_inscripciones_ramos.sql` - Inscripciones a secciones
- `21_pagos.sql` - Pagos y deudas
- `22_cuota.sql` - Cuotas de pago
- `23_transaccion_pago.sql` - Transacciones realizadas

### Fase 5: Tablas Puente (24-27)
- `24_estudiante_colegio.sql` - Relación estudiante-colegio
- `25_estudiante_direccion.sql` - Relación estudiante-dirección
- `26_ramo_areaConocimiento.sql` - Clasificación de ramos
- `27_ramosPlanEstudio_prerequisito.sql` - Prerequisitos en planes

## 🚀 Uso

### Opción 1: Carga Manual (MySQL)
```bash
# Desde MySQL CLI
mysql -u inacap_test -p inacap_test < database/seed_data/master_seed.sql
```

### Opción 2: Carga Automática (Pytest)
El archivo `conftest.py` carga automáticamente los datos al iniciar cada test:

```python
@pytest.fixture(scope="function")
def db():
    """Fixture que proporciona conexión a BD con datos semilla"""
    database = DatabaseManager()
    database.connect()
    database.clear_tables()
    database.load_seed_data()  # ← Carga automática
    yield database
    database.disconnect()
```

### Opción 3: Desde Python
```python
from testing.conftest import DatabaseManager

db = DatabaseManager()
db.connect()
db.clear_tables()
db.load_seed_data()
```

## 📊 Datos Disponibles

### Estudiantes (8 registros)
- RUT `20587683-9`: Camila Manríquez (Administración, con deuda)
- RUT `21195581-3`: Anahí Formantel (Odontología, sin deuda)
- RUT `21379413-2`: Dante Agüero (Analista Programador)
- Más 5 estudiantes adicionales...

### Carreras (3 registros)
- `AE`: Administración de Empresas
- `OD`: Técnico en Odontología
- `B5`: Analista Programador

### Ramos (10 registros)
- Matemáticas: MAT101, MAT102, MAT201
- Inglés: IDEN01, IDEN02, IDEN03
- Lenguaje: LEN101, LEN102
- Técnicos: TEC101, SAL101

## ✅ Ventajas

1. **Testing más rápido**: No necesitas insertar datos manualmente
2. **Datos consistentes**: Todos los tests usan los mismos datos base
3. **Relaciones completas**: Los datos tienen todas las FK necesarias
4. **Basados en datos reales**: Extraídos de los CSV proporcionados

## 🔧 Ejemplo de Test

```python
def test_estudiante_con_datos_semilla(db):
    """Test usando estudiante predefinido"""
    # Camila ya existe con id=1
    result = db.fetch_query(
        "SELECT nombre FROM Estudiante WHERE rut = %s",
        ('20587683-9',)
    )
    assert result[0][0] == 'Camila Ignacia Manríquez Delgado'
```

## ⚠️ Notas Importantes

1. **IDs Autoincrementales**: Usa los RUT o códigos en lugar de IDs para mayor consistencia
2. **Dependencias Circulares**: Matricula y Predictor_Datos tienen dependencia circular, ajustar si es necesario
3. **Actualización**: Ejecutar `master_seed.sql` limpia y recarga todos los datos

## 🔄 Actualización de Datos

Para agregar más datos semilla:
1. Edita el archivo SQL correspondiente
2. Ejecuta `master_seed.sql` para recargar
3. O recarga solo el archivo específico

---

**Autor**: Sistema de Testing INACAP  
**Última actualización**: Enero 2026
