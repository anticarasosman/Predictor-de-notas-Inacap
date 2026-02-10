# 📊 Herramienta de Consultas INACAP

Aplicación Windows para exportación y consulta de datos de estudiantes INACAP. Permite generar reportes en Excel con información académica, financiera y personalizada, además de lectura automatizada de certificados en PDF.

**Versión:** 2.0  
**Base de Datos:** AWS RDS MySQL 8.0  
**Plataforma:** Windows 10+  
**Estado:** ✅ Producción

---

## ✨ Características Principales

### 📋 Exportación de Datos
- **Reporte General**: Información demográfica y de contacto del estudiante
- **Información Académica**: Semestres cursados, asignaturas y calificaciones
- **Información Financiera**: Estado de cuenta, morosidad y pagos
- **Reportes Personalizados**: Crea tus propias hojas de cálculo seleccionando columnas específicas

### 📄 Lectura de Certificados PDF
- Extracción automática de calificaciones desde certificados de enseñanza media
- Reconocimiento automático de tipos: ANUAL y CONCENTRACIÓN
- Importación directa de datos al sistema

### 🎨 Gestión de Reportes Personalizados
- **Crear nuevos reportes**: Interfaz visual con selección de columnas por tabla
- **Eliminar reportes**: Gestionar los reportes guardados
- **Reutilizar reportes**: Carga los reportes personalizados en futuras exportaciones

---

## 🚀 INSTALACIÓN Y USO

### Requisitos Mínimos
- Windows 10 o superior
- 50 MB de espacio en disco
- Conexión a Internet (para conectar a AWS RDS)

### Instalación Rápida

1. **Descargar archivo ejecutable**
   - Descarga `Herramienta-Consultas-Inacap.exe`

2. **Configurar conexión a la base de datos**
   - En la misma carpeta que el .exe, crea un archivo llamado `.env`
   - Copia el siguiente contenido:
   ```
   DB_HOST=base-de-datos-inacap.cxeouo22gw7q.sa-east-1.rds.amazonaws.com
   DB_USER=admin
   DB_PASSWORD=tu_contraseña_aqui
   DB_NAME=inacap_test
   DB_PORT=3306
   ```
   - Reemplaza `tu_contraseña_aqui` con la contraseña proporcionada

3. **Ejecutar la aplicación**
   - Haz doble clic en `Herramienta-Consultas-Inacap.exe`
   - La interfaz se abrirá lista para usar

---

## � GUÍA DE USO

### 1️⃣ Buscar Estudiante
1. Abre la aplicación
2. En el campo de búsqueda, ingresa el **RUT del estudiante** (ej: 17.234.567-8)
3. Haz clic en "Buscar"
4. Los datos del estudiante se cargarán automáticamente

### 2️⃣ Exportar Datos a Excel
1. Selecciona los tipos de reporte que deseas incluir:
   - ☑️ **Información General**: Datos personales
   - ☑️ **Información Académica**: Calificaciones y semestres
   - ☑️ **Información Financiera**: Estado de cuenta
   - ☑️ **Reportes Personalizados**: Tus reportes guardados

2. Define el nombre del archivo Excel
3. Haz clic en "Exportar"
4. El archivo se guardará en tu carpeta de Descargas

### 3️⃣ Crear Reporte Personalizado
1. Haz clic en "Crear Reportes Personalizados"
2. Una ventana mostrará todas las tablas y columnas disponibles
3. Selecciona las columnas que deseas incluir
4. Escribe un nombre para el reportes
5. Haz clic en "Guardar Reportes"
6. El reportes estará disponible para futuras exportaciones

### 4️⃣ Eliminar Reporte Personalizado
1. Haz clic en "Eliminar Reportes Personalizados"
2. Selecciona el o los reportes que deseas eliminar
3. Haz clic en "Eliminar"
4. Confirma la eliminación

### 5️⃣ Leer Certificado PDF
1. Haz clic en "Leer Certificado"
2. Selecciona el archivo PDF del certificado
3. La aplicación detectará automáticamente el tipo (ANUAL o CONCENTRACIÓN)
4. Los datos se cargarán para revisión

---

## 🔐 SEGURIDAD Y CONFIGURACIÓN

### Archivo .env
El archivo `.env` contiene las credenciales de acceso a la base de datos:
- **DB_HOST**: Servidor de base de datos (AWS RDS)
- **DB_USER**: Usuario de acceso (`admin`)
- **DB_PASSWORD**: Contraseña (proporcionada por administrador)
- **DB_NAME**: Nombre de la base de datos (`inacap_test`)
- **DB_PORT**: Puerto de conexión (3306)

⚠️ **IMPORTANTE**: 
- Nunca compartas el archivo `.env` ni la contraseña
- Guarda este archivo en la misma carpeta que el ejecutable
- Si olvidas la contraseña, contacta al administrador IT

### Permisos
El usuario de acceso tiene permisos de:
- ✅ Lectura de datos (SELECT)
- ✅ Inserción de datos (INSERT)
- ✅ Actualización de datos (UPDATE)
- ❌ Eliminación de registros (protegido)



## 🛠️ SOLUCIÓN DE PROBLEMAS

| Problema | Solución |
|----------|----------|
| **"Error: archivo .env no encontrado"** | Verifica que el archivo `.env` esté en la misma carpeta que el .exe |
| **"Error: No se puede conectar a la base de datos"** | Verifica que tienes conexión a Internet y que la contraseña en .env es correcta |
| **"Error: Tabla no encontrada"** | Contacta al administrador IT - puede haber un problema con la base de datos |
| **La aplicación se abre lentamente** | Normal en las conexiones a AWS RDS. Espera 10 segundos para la primera conexión |
| **"Access denied for user 'admin'"** | La contraseña en .env es incorrecta. Solicita la contraseña al administrador |
| **El certificado PDF no se lee correctamente** | Asegúrate que el PDF contiene tablas de calificaciones estándar |

---

## 📊 FORMATO DE DATOS

### Información del Estudiante
La aplicación exporta:
- RUT
- Nombre completo
- Género
- Fecha de nacimiento
- Institución de procedencia
- Correo electrónico
- Teléfono

### Información Académica
- Semestre cursado
- Asignaturas
- Calificación por asignatura
- Créditos
- Estado académico

### Información Financiera
- Saldo actual
- Pagos realizados
- Cuotas morosas
- Deudas acumuladas
- Últimas 6 transacciones

---

## 📁 ESTRUCTURA DE ARCHIVOS

Después de instalar, tu carpeta contendrá:
```
Herramienta-Consultas-Inacap/
├── Herramienta-Consultas-Inacap.exe      - Aplicación principal
├── .env                                  - Configuración (creado por ti)
├── personalized_sheets/                  - Reportes personalizados (se crea automáticamente)
│   ├── reporte_1.json
│   ├── reporte_2.json
│   └── ...
└── datos_exportados/                     - Archivos Excel generados
    ├── Estudiante_XXXXX_2026-01-15.xlsx
    └── ...
```

---

## 📞 SOPORTE

Si encuentras problemas:

1. **Verifica la conexión a Internet**
   - La aplicación necesita conectar a AWS RDS en Sudamérica

2. **Comprueba el archivo .env**
   - Copia el contenido correctamente (sin espacios extras)
   - La contraseña debe ser la proporcionada por IT

3. **Reinicia la aplicación**
   - A veces los problemas de conexión se resuelven cerrando y reabriendo

4. **Contacta al administrador IT**
   - Incluye el mensaje de error exacto
   - Indica tu usuario y RUT del estudiante buscado

---

## 🔄 ACTUALIZACIONES

Cuando haya nuevas versiones:
1. Descarga la nueva versión de `Herramienta-Consultas-Inacap.exe`
2. Reemplaza el archivo anterior
3. Mantén tu archivo `.env` en la misma carpeta
4. Tus reportes personalizados se conservarán

---

## 📋 HISTORIAL DE VERSIONES

**v2.0** (Febrero 2026)
- ✨ Interfaz gráfica mejorada
- ✨ Conexión a AWS RDS
- ✨ Creación de reportes personalizados
- ✨ Lectura de certificados PDF
- ✨ Ajuste automático de ancho de columnas

**v1.0** (Versión inicial)
- Exportación básica de datos
- Reportes predeterminados

---

## 📄 LICENCIA Y USO

Esta herramienta es de uso exclusivo para INACAP.

- ✅ Permitido: Buscar datos de estudiantes autorizados
- ✅ Permitido: Exportar reportes para fines administrativos
- ❌ Prohibido: Compartir .exe o credenciales
- ❌ Prohibido: Modificar o redistribuir la aplicación
- ❌ Prohibido: Acceder a datos sin autorización

---

**Última actualización:** Febrero 2026  
**Desarrollado para:** Instituto Profesional INACAP

