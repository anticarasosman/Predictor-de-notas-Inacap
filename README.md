# Predictor De Notas INACAP

Sistema de prediccion de notas para estudiantes de INACAP con suite completa de testing.

---

## 🚀 SETUP RAPIDO (Nuevos usuarios)

### Requisitos previos
- MySQL Server 8.0+
- Python 3.10+
- PowerShell (Windows) o Terminal (Mac/Linux)

### 3 pasos para empezar

**Paso 1: Crear archivo .env**
```powershell
Copy-Item .env.example .env
```

**Paso 2: Instalar dependencias**
```bash
pip install -r requirements-testing.txt
```

**Paso 3: Ejecutar tests**
```bash
cd testing
python -m pytest . -v
```

**Resultado esperado:** `17 passed in X.XX seconds`

---

## 🔐 CONFIGURACION DE USUARIOS Y VARIABLES DE ENTORNO

### Usuarios MySQL creados

1. **inacap_app**
   - Proposito: Aplicacion principal
   - Permisos: SELECT, INSERT, UPDATE, DELETE en inacap_test
   - Contraseña: (ninguna - acceso local)
   - Uso: Usuarios finales del sistema

2. **inacap_test**
   - Proposito: Automatizacion de tests
   - Permisos: TODOS en inacap_test (para crear/drop/alter)
   - Contraseña: (ninguna - acceso local)
   - Uso: pytest y desarrollo

3. **inacap_admin**
   - Proposito: Administration del servidor
   - Permisos: TODOS en todas las bases de datos
   - Contraseña: Admin_Temporal_123 (CAMBIAR cuando sea posible)
   - Uso: Tareas administrativas y mantenimiento

### Archivo .env

Ubicacion: Carpeta raiz del proyecto
Contenido:
```
DB_HOST=localhost
DB_USER=inacap_test
DB_PASSWORD=
DB_NAME=inacap_test
DB_PORT=3306
```

**IMPORTANTE:** .env esta en .gitignore (nunca se sube al repositorio)

---

## 👤 SETUP INICIAL (Para el Admin)

Este procedimiento debe ejecutarse **UNA SOLA VEZ** cuando se configura el servidor. Si la base de datos ya esta creada dejo estas instrucciones para dejar registro de lo que hice

### Paso 1: Crear la base de datos

```bash
mysql -u root -p < database/set_up.sql
```

Ingresa la contraseña de root.

### Paso 2: Crear los usuarios MySQL

```powershell
$env:Path += ";C:\Program Files\MySQL\MySQL Server 8.0\bin"
Get-Content database/create_app_users.sql | mysql -u root -p
```

Ingresa la contraseña de root.

### Paso 3: Verificar que los usuarios fueron creados

```bash
mysql -u root -p -e "SELECT USER FROM mysql.user WHERE USER LIKE 'inacap%';"
```

Resultado esperado:
```
+--------------+
| USER         |
+--------------+
| inacap_admin |
| inacap_app   |
| inacap_test  |
+--------------+
```

### Paso 4: Probar conexion como inacap_test

```bash
mysql -u inacap_test -h localhost inacap_test
```

Dentro de mysql:
```sql
SHOW TABLES;
EXIT;
```

Deberias ver las 9 tablas: Region, Comuna, Colegio, Estudiante, etc.

### Paso 5: Cambiar contraseña de admin (RECOMENDADO)

```bash
mysql -u inacap_admin -pAdmin_Temporal_123 -h localhost
```

Luego ejecuta:
```sql
ALTER USER 'inacap_admin'@'localhost' IDENTIFIED BY 'tu_contraseña_fuerte_aqui';
EXIT;
```

### Paso 6: Instalar dependencias Python

```bash
pip install -r requirements-testing.txt
```

### Paso 7: Crear .env para ti

```powershell
Copy-Item .env.example .env
```

### Paso 8: Ejecutar tests para verificar

```bash
cd testing
python -m pytest . -v
```

Resultado esperado: `17 passed in X.XX seconds`

---

## 🧪 TESTING DE BASE DE DATOS

### Tests incluidos (18 total)

#### ✅ Datos Validos (6 tests)
Verifican que se pueden insertar datos correctamente:
- test_insertar_region
- test_insertar_multiple_regiones
- test_insertar_comuna
- test_insertar_colegio_completo
- test_insertar_estudiante
- test_insertar_estudiante_direccion_bridge

#### ❌ Datos Invalidos (7 tests)
Verifican que se rechazan datos invalidos:
- test_region_codigo_duplicado
- test_region_nombre_duplicado
- test_comuna_sin_region
- test_colegio_sin_comuna
- test_estudiante_email_duplicado
- test_estudiante_rut_duplicado
- test_colegio_rbd_duplicado

#### 🔄 CASCADE y RESTRICT (5 tests)
Verifican que las reglas de eliminacion funcionan:
- test_restrict_eliminar_region_con_comunas
- test_restrict_eliminar_comuna_con_colegios
- test_cascade_eliminar_estudiante_elimina_historial
- test_cascade_eliminar_estudiante_colegio
- test_restrict_eliminar_colegio_con_estudiantes

### Comandos utiles

```bash
# Ejecutar todos los tests
python -m pytest . -v

# Ejecutar solo tests de datos validos
python -m pytest tests_de_inserciones_validas/ -v

# Ejecutar solo tests de datos invalidos
python -m pytest tests_de_inserciones_invalidas/ -v

# Ejecutar solo CASCADE/RESTRICT
python -m pytest tests_de_cascade_y_restrict/ -v

# Ver output detallado
python -m pytest . -v -s

# Ver ejemplos practicos
python ejemplos_testing.py
```

### Clase DatabaseManager

Ubicacion: `testing/conftest.py`

Uso basico:
```python
# El fixture 'db' esta disponible automaticamente en todos los tests
def test_ejemplo(db):
    # Conectar (automatico por fixture)
    # db esta conectado y las tablas estan limpias
    
    # Insertar/Actualizar/Eliminar
    success, error = db.execute_query(query, values)
    if success:
        print("✓ Exitoso")
    else:
        print(f"✗ Error: {error}")
    
    # Consultar
    result = db.fetch_query(query, values)
    for row in result:
        print(row)
    
    # Desconectar (automatico al finalizar el test)
```

Para uso manual (fuera de tests):
```python
from testing.conftest import DatabaseManager

# Conectar
db = DatabaseManager()
db.connect()

# Insertar/Actualizar/Eliminar
success, error = db.execute_query(query, values)

# Consultar
result = db.fetch_query(query, values)

# Limpiar
db.clear_tables()

# Desconectar
db.disconnect()
```

---

## 📁 ESTRUCTURA DEL PROYECTO

```
testing/
├── conftest.py                           - DatabaseManager + pytest fixture compartida
├── __init__.py                           - Paquete pytest
├── ejemplos_testing.py                   - 6 ejemplos practicos
├── requirements-testing.txt              - Dependencias
│
├── tests_de_inserciones_validas/         - 6 tests de inserciones correctas
│   ├── __init__.py
│   └── test_validas.py
│       ├── test_insertar_region
│       ├── test_insertar_multiple_regiones
│       ├── test_insertar_comuna
│       ├── test_insertar_colegio_completo
│       ├── test_insertar_estudiante
│       └── test_insertar_estudiante_direccion_bridge
│
├── tests_de_inserciones_invalidas/       - 7 tests de validaciones y constraints
│   ├── __init__.py
│   └── test_invalidas.py
│       ├── test_region_codigo_duplicado
│       ├── test_region_nombre_duplicado
│       ├── test_comuna_sin_region
│       ├── test_colegio_sin_comuna
│       ├── test_estudiante_email_duplicado
│       ├── test_estudiante_rut_duplicado
│       └── test_colegio_rbd_duplicado
│
└── tests_de_cascade_y_restrict/          - 5 tests de reglas de eliminacion
    ├── __init__.py
    └── test_cascade_restrict.py
        ├── test_restrict_eliminar_region_con_comunas
        ├── test_restrict_eliminar_comuna_con_colegios
        ├── test_cascade_eliminar_estudiante_elimina_historial
        ├── test_cascade_eliminar_estudiante_colegio
        └── test_restrict_eliminar_colegio_con_estudiantes

database/
├── set_up.sql                    - Crear BD y tablas
├── create_app_users.sql          - Crear usuarios MySQL
├── master.sql
├── schema/                       - Definicion de tablas
├── indexes/                      - Indices
├── views/                        - Vistas
└── triggers/                     - Triggers

instrucciones_testing/
├── SETUP_RAPIDO.txt              - Para nuevos usuarios
├── ADMIN_SETUP_INICIAL.txt       - Para el admin
├── CONFIGURACION_USUARIOS.txt    - Detalles de seguridad
├── TESTING_GUIDE.md              - Guia tecnica
└── TESTING_QUICKSTART.txt        - Resumen visual
```


## 🛠️ TROUBLESHOOTING

| Error | Solucion |
|-------|----------|
| `ModuleNotFoundError: No module named 'pytest'` | `pip install pytest` |
| `ModuleNotFoundError: No module named 'mysql'` | `pip install mysql-connector-python` |
| `ModuleNotFoundError: No module named 'dotenv'` | `pip install python-dotenv` |
| `Unknown database 'inacap_test'` | `mysql -u root -p < database/set_up.sql` |
| `Access denied for user 'inacap_test'` | Verifica que .env tiene DB_USER=inacap_test |
| `mysql: El termino 'mysql' no se reconoce` | Agrega MySQL al PATH: `$env:Path += ";C:\Program Files\MySQL\MySQL Server 8.0\bin"` |


## 📊 REGLAS DE NEGOCIO

### Relacion alumno-colegio
1. No se permite eliminar un colegio mientras aun existan relaciones alumno-colegio (RESTRICT).
2. Si se elimina un alumno entonces tambien se elimina todas sus relaciones con los colegios en los que ha estado (CASCADE).

### Integridad referencial
- Cada comuna debe tener una region valida (Foreign Key)
- Cada colegio debe tener una comuna valida (Foreign Key)
- Cada estudiante debe tener datos validos (UNIQUE en email y RUT)

---
