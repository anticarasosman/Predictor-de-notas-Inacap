# Migración a API Gateway - Resumen

## ✅ Cambios Completados

### 1. DatabaseConnection Modificado
**Archivo:** `database/db_connection.py`

**Cambios principales:**
- ✅ Reemplazado `mysql.connector` por `APIClient`
- ✅ Constructor ahora usa `API_URL` y `API_TIMEOUT` del `.env`
- ✅ Método `connect()` verifica API Gateway en lugar de MySQL
- ✅ Agregados métodos CRUD completos:
  - `listar_estudiantes(filtros, pagina, limite)` → Retorna tupla (List[Dict], metadatos)
  - `buscar_estudiante(rut)` → Retorna Optional[Dict]
  - `insertar_estudiante(datos)` → Retorna Dict
  - `actualizar_estudiante(rut, datos)` → Retorna Dict
  - `eliminar_estudiante(rut)` → Retorna Dict
  - `consulta_personalizada(tabla, columnas, filtros, pagina, limite)`
  - `insertar_generico(tabla, datos)`
  - `actualizar_generico(tabla, id_campo, id_valor, datos)`
  - `eliminar_generico(tabla, id_campo, id_valor)`

**Métodos deprecados (lanzan NotImplementedError):**
- ❌ `cursor()` - Ya no retorna cursor MySQL
- ❌ `get_connection()` - Ya no retorna conexión MySQL
- ❌ `execute_query()` - Ya no ejecuta SQL directo
- ❌ `fetch_query()` - Ya no ejecuta SELECT directo

### 2. Configuración Actualizada

**Archivo:** `.env`
```env
API_URL=https://r9862991zc.execute-api.sa-east-1.amazonaws.com/prod/consultar
API_TIMEOUT=30
```

**Archivo:** `.env.example`
- ✅ Documentado formato de configuración API
- ✅ Variables MySQL movidas a sección "ANTIGUO" con comentarios

### 3. Tests de Validación

**Archivo:** `test_db_connection_api.py`
- ✅ Valida inicialización con API_URL
- ✅ Valida conexión a API Gateway
- ✅ Valida que métodos deprecados lanzan NotImplementedError
- ✅ Verifica manejo de errores (HTTP 500 esperado - tabla no existe)

**Resultado de tests:**
```
✓ DatabaseConnection inicializado correctamente
✓ Conexión exitosa a API Gateway
✓ Estado: CONECTADO
✓ Métodos deprecados funcionan correctamente
✓ Desconexión exitosa
```

## 📋 Próximos Pasos

### Paso 1: Actualizar Clases Reader
**Archivos a modificar:** Todos los que usen `DatabaseConnection`

**Cambio principal:** Resultados de **MySQL cursors (tuplas)** → **Diccionarios JSON**

#### Antes (MySQL cursor):
```python
cursor = db.cursor()
cursor.execute("SELECT rut, nombre, email FROM estudiante WHERE rut = %s", (rut,))
resultado = cursor.fetchone()
if resultado:
    rut = resultado[0]      # Acceso por índice
    nombre = resultado[1]
    email = resultado[2]
```

#### Después (API):
```python
estudiante = db.buscar_estudiante(rut)
if estudiante:
    rut = estudiante["rut"]        # Acceso por clave
    nombre = estudiante["nombre"]
    email = estudiante["email"]
```

#### Ejemplo de migración para listar:
```python
# Antes
cursor = db.cursor()
cursor.execute("SELECT * FROM estudiante WHERE activo = 1")
estudiantes = cursor.fetchall()

# Después
estudiantes, metadatos = db.listar_estudiantes(
    filtros={"activo": True},
    pagina=1,
    limite=100
)
# estudiantes es List[Dict]
# metadatos tiene: {"total": 250, "pagina": 1, "limite": 100, "paginas_totales": 3}
```

### Paso 2: Encontrar Archivos que Usan db_connection

**Comando para buscar:**
```powershell
grep -r "DatabaseConnection" --include="*.py" .
grep -r "cursor()" --include="*.py" .
grep -r "fetchone\|fetchall" --include="*.py" .
```

**Archivos candidatos probables:**
- `classes/*.py` (clases de negocio)
- `load_data/*.py` (carga de datos)
- `main.py` o archivos GUI principales

### Paso 3: Manejo de Errores

**Cambiar de:**
```python
from mysql.connector import Error

try:
    # operación base de datos
except Error as e:
    print(f"Error MySQL: {e}")
```

**A:**
```python
from aws.api_client import APIClientError

try:
    # operación base de datos
except APIClientError as e:
    print(f"Error API: {e}")
```

### Paso 4: Actualizar PyInstaller

**Archivo:** `Herramienta-Consultas-Inacap.spec`

**Agregar:**
```python
hiddenimports=[
    'requests',           # ← AGREGAR (para APIClient)
    'urllib3',            # ← AGREGAR (dependencia de requests)
    'certifi',            # ← AGREGAR (certificados SSL)
    # ... otros imports existentes
],
```

**Remover (ya no necesarios):**
```python
# mysql.connector
# mysql.connector.locales
# Colección de locales MySQL (Tree analysis)
```

### Paso 5: Crear Tablas en RDS

**Actualmente:** Base de datos `inacap_test` está VACÍA
**Por eso:** Tests retornan HTTP 500 "Table doesn't exist"

**Opciones:**
1. Ejecutar scripts SQL en `database/schema/`
2. Ejecutar `database/seed_data/master_seed.sql`
3. Usar herramienta de administración MySQL

**Comando (desde máquina con acceso MySQL):**
```bash
mysql -h base-de-datos-inacap.cxeouo22gw7q.sa-east-1.rds.amazonaws.com \
      -u admin -p \
      inacap_test < database/schema/core/estudiante.sql
```

### Paso 6: Testing Completo

1. **Unit tests:** Validar cada clase modificada
2. **Integration tests:** Validar flujo completo con API
3. **GUI tests:** Validar interfaz usuario con datos reales
4. **Network tests:** Probar desde redes corporativas (puerto 443 HTTPS)

### Paso 7: Compilar Nueva Versión

```powershell
# Recompilar con PyInstaller
pyinstaller Herramienta-Consultas-Inacap.spec --clean

# Versión sugerida: v3.0 (arquitectura serverless)
```

## 🔍 Checklist de Migración

### Infraestructura ✅
- [x] Lambda function creada y desplegada
- [x] API Gateway configurada con CORS
- [x] APIClient implementado (400 líneas)
- [x] DatabaseConnection migrado a API
- [x] Tests de infraestructura pasando

### Configuración ✅
- [x] .env actualizado con API_URL
- [x] .env.example documentado
- [x] Variables MySQL comentadas/removidas

### Código de Aplicación ⬜
- [ ] Identificar archivos que usan DatabaseConnection
- [ ] Migrar acceso de tuplas a diccionarios
- [ ] Cambiar mysql.connector.Error → APIClientError
- [ ] Actualizar imports
- [ ] Actualizar validación de resultados

### Build y Deploy ⬜
- [ ] Actualizar spec de PyInstaller
- [ ] Agregar requests a hiddenimports
- [ ] Remover mysql.connector
- [ ] Compilar .exe v3.0
- [ ] Validar tamaño del ejecutable

### Testing ⬜
- [ ] Crear tablas en RDS
- [ ] Insertar datos de prueba
- [ ] Tests unitarios con datos reales
- [ ] Tests de interfaz gráfica
- [ ] Tests desde red corporativa

### Seguridad ⚠️
- [ ] Rotar password RDS (actualmente expuesto)
- [ ] Restringir Security Group (actualmente 0.0.0.0/0)
- [ ] Implementar API keys en API Gateway
- [ ] Agregar rate limiting

### Documentación ⬜
- [ ] Actualizar README.md (v3.0)
- [ ] Guía de troubleshooting API
- [ ] Instrucciones para usuarios finales
- [ ] Documentar arquitectura serverless

## 📊 Comparación Antes/Después

### Instalación de Usuario

#### v2.7 (SSH Tunnel):
```
1. Descargar .zip (47 MB)
2. Extraer archivos
3. Copiar .env con DB_HOST, DB_PORT, DB_USER, DB_PASSWORD
4. Copiar tunnel-inacap.pem
5. Ejecutar iniciar-con-tunel.bat
6. Esperar que SSH tunnel conecte
7. Usar aplicación
```

#### v3.0 (API Gateway):
```
1. Descargar .zip (~50 MB estimado)
2. Extraer archivos
3. Ejecutar .exe directamente
   (API_URL incluido internamente o en .env simple)
4. Usar aplicación
```

### Características

| Característica | v2.7 (Tunnel) | v3.0 (API) |
|----------------|---------------|------------|
| **Archivos requeridos** | .exe + .env + .pem | .exe solamente |
| **Puerto** | 3306 (bloqueado) + SSH en 443 | 443 HTTPS (nunca bloqueado) |
| **Configuración** | Compleja | Simple |
| **Seguridad** | Credenciales expuestas | Ocultas en Lambda |
| **Mantenimiento** | EC2 siempre corriendo | Serverless (sin servidores) |
| **Escalabilidad** | Limitada | Automática |
| **Costo mensual** | ~$8 (EC2 t2.micro) | ~$0-2 (Lambda free tier) |

## 🎯 Ventajas de la Migración

1. **Simplicidad:** Un solo .exe, sin configuración
2. **Seguridad:** Credenciales nunca expuestas al cliente
3. **Accesibilidad:** HTTPS puerto 443 accesible desde cualquier red
4. **Escalabilidad:** Lambda escala automáticamente
5. **Costo:** Más económico (sin EC2 corriendo 24/7)
6. **Mantenimiento:** No requiere administrar servidores

## ⚠️ Notas Importantes

- Los métodos `cursor()`, `execute_query()`, `fetch_query()` ya NO funcionan
- Todo código que use SQL directo debe migrar a métodos específicos
- Resultados ahora son diccionarios, no tuplas de MySQL
- Paginación es obligatoria para datasets grandes (límite en Lambda)
- Timeout máximo: 30 segundos por petición (configurable en .env)

## 📞 Soporte

Si hay problemas durante la migración:
1. Verificar `.env` tiene `API_URL` correcta
2. Verificar conexión: `python test_db_connection_api.py`
3. Revisar logs de Lambda en CloudWatch
4. Validar que tablas existen en RDS
