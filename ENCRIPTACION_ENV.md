# Sistema de Encriptación del Archivo .env

## 📋 Descripción

Este proyecto implementa encriptación automática del archivo `.env` para proteger las credenciales de la base de datos cuando se distribuye la aplicación.

## 🔐 Componentes

### 1. `config_loader.py`
Módulo que desencripta automáticamente `.env.encrypted` al iniciar la aplicación.
- **Clave hardcodeada**: `XHPMYwkt9o5KW88IS9IWhvatduAK7issto2Zw2UHiAo=`
- **Sin intervención del usuario**: La desencriptación es transparente
- **Algoritmo**: Fernet (AES-128 CBC con HMAC)

### 2. `encrypt_env.py`
Script para generar el archivo `.env.encrypted` desde `.env`

**Uso:**
```bash
python encrypt_env.py
```

**Output:**
- Genera `.env.encrypted` (908 bytes)
- Este archivo se incluye en la distribución

### 3. Modificaciones en `main.py`
- ✅ Reemplazado `from dotenv import load_dotenv` por `import config_loader`
- ✅ Reemplazado `load_dotenv(env_path)` por `config_loader.load_config()`

## 🚀 Flujo de Trabajo

### Desarrollo (con .env original)
1. Mantener `.env` en el directorio del proyecto (NO subir a Git)
2. Ejecutar `python encrypt_env.py` para generar/actualizar `.env.encrypted`
3. La aplicación usa `.env.encrypted` automáticamente

### Distribución (PyInstaller)
1. El archivo `.env.encrypted` se incluye en el ejecutable
2. El archivo `.env` original NO se distribuye
3. Al ejecutar, `config_loader.py` desencripta automáticamente

## 📦 Compilación con PyInstaller

El archivo `Herramienta-INACAP-v3.0.spec` ya incluye:
- ✅ `config_loader.py` en los archivos
- ✅ `.env.encrypted` en los datos
- ✅ `cryptography` en hiddenimports

**Compilar:**
```bash
pyinstaller "Herramienta-INACAP-v3.0.spec" --clean --noconfirm
```

## 🔒 Seguridad

### ⚠️ IMPORTANTE
- La clave está hardcodeada en el código fuente
- **NO es una solución para repositorios públicos**
- Protege contra usuarios finales que descarguen el ejecutable
- NO protege contra ingeniería inversa del ejecutable

### Para mayor seguridad (futuras mejoras):
1. Usar variables de entorno para la clave
2. Implementar key derivation con contraseña del usuario
3. Usar HSM o servicios de gestión de secretos (AWS Secrets Manager)

## 📝 Archivos Modificados

| Archivo | Modificación |
|---------|--------------|
| `main.py` | Usa `config_loader` en lugar de `dotenv` |
| `.gitignore` | Permite `.env.encrypted` con `!.env.encrypted` |
| `Herramienta-INACAP-v3.0.spec` | Incluye archivos de encriptación |

## ✅ Validación

**Probar en desarrollo:**
```bash
python main.py
```

**Output esperado:**
```
[CONFIG] Buscando .env.encrypted en: C:\...\Predictor-de-notas-Inacap\.env.encrypted
[CONFIG] ✓ Archivo .env.encrypted desencriptado y cargado exitosamente
[DB] Intentando conectar...
✓ Conectado a: admin@base-de-datos-inacap...
```

## 🔄 Actualizar Credenciales

Si cambias las credenciales en `.env`:
1. Modificar `.env`
2. Ejecutar `python encrypt_env.py`
3. Verificar que `.env.encrypted` se actualizó
4. Recompilar con PyInstaller si es necesario

---

**Fecha de implementación:** Febrero 19, 2026  
**Versión:** 3.0
