# Implementación: Sistema de Captura de Métricas de Morosidad

## Cambios Implementados

### 1. Nueva Tabla: `Resumen_reporte_morosidad`
**Archivo:** `database/schema/core/resumen_reporte_morosidad.sql`

Almacena un resumen resumido de métricas de morosidad con los siguientes campos:
- **fecha_actualizacion**: Fecha de los datos procesados (UNIQUE)
- **numero_estudiantes_total**: Total de estudiantes en el reporte
- **numero_estudiantes_con_deuda**: Cantidad de estudiantes con deuda > $0
- **porcentaje_estudiantes_con_deuda**: (deudores / total) * 100
- **monto_total_adeudado**: Suma de columna "Total Saldo"
- **monto_total_compromisos**: Suma de "Monto Compromiso Matricula" + "Monto Compromisos Colegiaturas"
- **promedio_cuotas_pendientes**: Promedio de "Cantidad Cuotas Pendientes Colegiaturas" (solo > 0)
- **porcentaje_morosidad**: (monto_total_adeudado / monto_total_compromisos) * 100

### 2. Tabla Actualizada: `Reporte_financiero_estudiante`
**Archivo:** `database/schema/core/reporte_financiero_estudiante.sql`

Se agregaron dos nuevos campos para almacenar compromisos a nivel de estudiante:
- **monto_compromiso_matricula**: Del CSV "Monto Compromiso Matricula"
- **monto_compromiso_colegiaturas**: Del CSV "Monto Compromisos Colegiaturas"

### 3. Clase Reader Actualizada
**Archivo:** `classes/readers/reader.py`

- El método `_insert_reporte_financiero()` ahora incluye los nuevos campos de compromiso

### 4. ReporteMorosidadReader Mejorado
**Archivo:** `classes/readers/excel_reader/reporte_morosidad_reader.py`

**Cambios principales:**
- Agregada importación de `datetime`
- Agregado atributo `self.metricas_morosidad` para almacenar métricas calculadas
- Datos de compromisos capturados en `datos_reporte_financiero_estudiante`
- Nuevo método `_calculate_and_insert_morosidad_summary()` que:
  - Calcula todas las métricas después de procesar todos los registros
  - Inserta/actualiza un resumen en `Resumen_reporte_morosidad`
  - Almacena métricas en `self.metricas_morosidad` para acceso posterior
  - Usa `ON DUPLICATE KEY UPDATE` para actualizar si ya existe una entrada para la fecha

### 5. Setup Database Actualizado
**Archivo:** `database/set_up.sql`

Se agregó la línea:
```sql
SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/schema/core/resumen_reporte_morosidad.sql;
```

## Flujo de Datos

1. **Lectura del CSV**: El `ReporteMorosidadReader` carga el archivo REPORTE MOROSIDAD
2. **Procesamiento por registro**: Para cada estudiante:
   - Inserta/actualiza datos en `Estudiante`
   - Inserta/actualiza datos financieros en `Reporte_financiero_estudiante` (incluyendo compromisos)
3. **Cálculo de métricas**: Después de procesar todos los registros:
   - Calcula 8 métricas clave de morosidad
   - Inserta resumen en `Resumen_reporte_morosidad`
   - Almacena métricas en memoria para acceso posterior

## Acceso a Métricas

Después de ejecutar `reader._process_and_upsert()`, las métricas están disponibles en:
```python
reader.metricas_morosidad = {
    'fecha_actualizacion': date(2026, 2, 6),
    'numero_estudiantes_total': 99,
    'numero_estudiantes_con_deuda': X,
    'porcentaje_estudiantes_con_deuda': X.XX,
    'monto_total_adeudado': XXXXX,
    'monto_total_compromisos': XXXXX,
    'promedio_cuotas_pendientes': X.XX,
    'porcentaje_morosidad': XX.XX
}
```

También se almacenan permanentemente en la BD en la tabla `Resumen_reporte_morosidad`.

## Test

Se creó `test_morosidad_reader.py` para verificar:
- Carga correcta del CSV
- Cálculo correcto de métricas
- Inserción en la base de datos
- Validación de datos almacenados
