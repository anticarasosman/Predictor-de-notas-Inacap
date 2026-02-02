# Docker Setup para Predictor de Notas INACAP

## 📋 Requisitos
- Docker Desktop instalado y corriendo
- PowerShell o terminal

## 🚀 Pasos para levantar la BD

### 1. Copiar variables de entorno
```powershell
Copy-Item .env.example .env
```

### 2. Construir la imagen y levantar el contenedor
```powershell
docker-compose up -d
```

**Paciencia:** La primera vez toma ~1-2 minutos mientras descarga MySQL e inicializa las tablas.

### 3. Verificar que la BD está lista
```powershell
docker-compose logs db
```

Busca este mensaje: `[System] [MY-013252] [Server] Ready for connections`

### 4. Conectar desde Python
```python
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

connection = mysql.connector.connect(
    host=os.getenv('DB_HOST'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_NAME'),
    port=int(os.getenv('DB_PORT', 3306))
)

cursor = connection.cursor()
cursor.execute("SELECT DATABASE()")
print(cursor.fetchone())  # Debería mostrar ('inacap_db',)
```

## 🛑 Comandos útiles

**Ver logs en tiempo real:**
```powershell
docker-compose logs -f db
```

**Detener la BD (preserva datos):**
```powershell
docker-compose down
```

**Resetear todo (borra datos):**
```powershell
docker-compose down -v
docker-compose up -d
```

**Acceder a MySQL desde terminal:**
```powershell
docker exec -it inacap-db mysql -u root -proot inacap_db
```

**Ejecutar script SQL:**
```powershell
docker exec -i inacap-db mysql -u root -proot inacap_db < database/set_up.sql
```

## 🐛 Troubleshooting

### Puerto 3306 ya en uso
```powershell
# Buscar qué usa el puerto
netstat -ano | findstr :3306

# O cambiar en docker-compose.yml:
# ports:
#   - "3307:3306"  <- cambiar primer número
```

### BD no inicializa correctamente
```powershell
# Limpiar y reintentar
docker-compose down -v
docker-compose up -d --build
```

### Conexión rechazada desde Python
```powershell
# Verificar que el contenedor está corriendo
docker ps

# Ver logs
docker-compose logs db
```

## 📦 Instalaciones necesarias en Python
```powershell
pip install python-dotenv mysql-connector-python
```

## 🔐 Seguridad

**⚠️ IMPORTANTE:** `.env.example` es solo referencia. 

Para producción:
- ✓ Cambiar credenciales en `.env`
- ✓ Usar secretos de Docker/Kubernetes
- ✓ NO subir `.env` al repo (ya está en `.gitignore`)
