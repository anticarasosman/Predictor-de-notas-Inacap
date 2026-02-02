# Guía de Readers - Carga de Datos a Base de Datos

## Concepto General

Un **Reader** es una clase que:
1. Lee un archivo CSV/XLSX
2. Procesa y limpia los datos
3. Inserta los datos en la base de datos MySQL

## Estructura de un Reader

```
Reader (clase abstracta)
    ├── read()  ← Método principal que coordina todo
    ├── _load_file()  ← Lee el archivo
    ├── _clean_data()  ← Limpia y procesa datos
    └── _insert_into_database()  ← Inserta en BD
```

## Ejemplo: AsignaturaCriticasReader

### 1. Definición de la clase

```python
from classes.readers.reader import Reader

class AsignaturaCriticasReader(Reader):
    def __init__(self, file_path: str, db_connection):
        self.file_path = file_path
        self.db_connection = db_connection
        self.data = None
```

### 2. Método read() - Orquestador Principal

```python
def read(self):
    """Lee el archivo y crea registros en la base de datos"""
    try:
        # 1. LEER EL ARCHIVO
        self.data = self._load_file()
        
        # 2. PROCESAR Y LIMPIAR DATOS
        self.data = self._clean_data()
        
        # 3. INSERTAR EN BASE DE DATOS
        self._insert_into_database()
        
        return True
    except Exception as e:
        print(f"Error: {str(e)}")
        return False
```

### 3. Leer el Archivo

```python
def _load_file(self) -> pd.DataFrame:
    """Carga CSV o XLSX"""
    if self.file_path.endswith('.csv'):
        df = pd.read_csv(self.file_path, sep=';', encoding='utf-8', skiprows=5)
    elif self.file_path.endswith('.xlsx'):
        df = pd.read_excel(self.file_path, skiprows=5)
    return df
```

### 4. Limpiar Datos

```python
def _clean_data(self) -> pd.DataFrame:
    """Limpia y prepara datos"""
    # Remover filas vacías
    self.data = self.data.dropna(how='all')
    
    # Rellenar NaN
    self.data['COLUMNA'] = self.data['COLUMNA'].fillna(0)
    
    # Convertir tipos
    self.data['NUMERO'] = pd.to_numeric(self.data['NUMERO'], errors='coerce')
    
    return self.data
```

### 5. Insertar en Base de Datos

```python
def _insert_into_database(self):
    """Itera sobre los datos e inserta cada fila"""
    cursor = self.db_connection.cursor()
    
    try:
        for index, row in self.data.iterrows():
            # Procesar cada fila
            self._insert_asignatura(cursor, row)
            self._insert_semestre(cursor, row)
            self._insert_asignatura_semestre(cursor, row)
        
        # Confirmar cambios
        self.db_connection.commit()
        
    except Error as e:
        self.db_connection.rollback()
        raise
    finally:
        cursor.close()
```

## Cómo Usar un Reader

```python
from database.db_connection import DatabaseConnection
from classes.readers.asignaturas_criticas_reader import AsignaturaCriticasReader

# 1. Crear conexión
db = DatabaseConnection(
    host='localhost',
    user='root',
    password='contraseña',
    database='predictor_notas'
)
db.connect()

# 2. Crear y usar reader
reader = AsignaturaCriticasReader(
    file_path='data/Asignaturas Críticas.csv',
    db_connection=db.get_connection()
)
reader.read()

# 3. Cerrar conexión
db.disconnect()
```

## Datos Necesarios para Cada Reader

### ReporteMorosidadReader
- **Archivo:** `REPORTE MOROSIDAD ALUMNOS ENERO 2026(Sheet1).csv`
- **Tablas destino:** 
  - `Estudiante`
  - `Reporte_financiero_estudiante`
- **Datos clave:** RUT, Deuda, Cuotas pendientes, Beneficios

### SeguimientoDeAlumnosReader
- **Archivo:** `Seguimiento de Alumnos.csv`
- **Tablas destino:**
  - `Estudiante`
  - `Estudiante_Asignatura`
- **Datos clave:** RUT, Asignatura, Notas, Asistencia, Riesgo

### SituacionAcademicaReader
- **Archivo:** `Situación Académica.csv`
- **Tablas destino:**
  - `Estudiante`
  - `Estudiante_Semestre`
- **Datos clave:** RUT, Asignaturas, Reprobaciones, Gratuidad

## Pasos para Implementar un Nuevo Reader

### 1. Crear archivo en `classes/readers/[nombre]_reader.py`

```python
from classes.readers.reader import Reader
import pandas as pd

class TuReaderReader(Reader):
    def __init__(self, file_path: str, db_connection):
        self.file_path = file_path
        self.db_connection = db_connection
        self.data = None
```

### 2. Implementar métodos

```python
    def read(self):
        try:
            self.data = self._load_file()
            self.data = self._clean_data()
            self._insert_into_database()
            return True
        except Exception as e:
            print(f"Error: {str(e)}")
            return False
    
    def _load_file(self) -> pd.DataFrame:
        # Tu lógica de carga
        pass
    
    def _clean_data(self) -> pd.DataFrame:
        # Tu lógica de limpieza
        pass
    
    def _insert_into_database(self):
        # Tu lógica de inserción
        pass
```

### 3. Métodos auxiliares para inserción

```python
    def _insert_tabla_principal(self, cursor, row):
        """Inserta en tabla principal"""
        check_query = "SELECT id FROM Tabla WHERE id = %s"
        cursor.execute(check_query, (row['ID'],))
        
        if cursor.fetchone():
            return  # Ya existe
        
        insert_query = "INSERT INTO Tabla (...) VALUES (...)"
        cursor.execute(insert_query, valores)
```

## Notas Importantes

1. **Manejo de duplicados:** Siempre verificar si el registro ya existe antes de insertar
2. **Transacciones:** Usar `commit()` para guardar cambios y `rollback()` en caso de error
3. **Conversión de datos:** Usar `pd.to_numeric()`, `pd.to_datetime()` para conversiones
4. **NaN values:** Rellenar con `fillna()` antes de insertar en BD
5. **Logging:** Agregar mensajes de progreso con `print()` o logging

## Dependencias Requeridas

```bash
pip install pandas
pip install mysql-connector-python
pip install openpyxl  # Para archivos XLSX
```

## Troubleshooting

### Error: "MySQL connection not available"
```python
# Verificar conexión antes de usar
if not db.is_connected():
    db.connect()
```

### Error: "Unknown column" en SQL
```python
# Verificar que nombres de columnas en CSV coincidan con tabla
# Usar strip() para remover espacios
row['COLUMNA'].strip()
```

### Error: "Incorrect integer value"
```python
# Convertir a tipo correcto
valor = int(row['COLUMNA']) if pd.notna(row['COLUMNA']) else 0
```

## Ejemplo Completo de Uso

```python
from database.db_connection import DatabaseConnection
from classes.readers.asignaturas_criticas_reader import AsignaturaCriticasReader
from classes.readers.reporte_morosidad_reader import ReporteMorosidadReader

# Conexión única para todos los readers
db = DatabaseConnection()
if not db.connect():
    exit(1)

try:
    # Usar múltiples readers
    readers = [
        AsignaturaCriticasReader('data/Asignaturas Críticas.csv', db.get_connection()),
        ReporteMorosidadReader('data/REPORTE MOROSIDAD.csv', db.get_connection()),
        # ... más readers
    ]
    
    for reader in readers:
        print(f"\nProcesando {reader.__class__.__name__}...")
        reader.read()

finally:
    db.disconnect()
```
