# 📊 Herramienta de Consultas INACAP

Aplicación Windows para exportación y consulta de datos de estudiantes INACAP. Permite generar reportes en Excel con información académica, financiera y personalizada, además de lectura automatizada de certificados en PDF.

**Base de Datos:** AWS RDS MySQL 8.0  
**Plataforma:** Windows 10+  

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
   - Descarga `Herramienta-Consultas-Inacap.zip`

2. **Configurar conexión a la base de datos**
   - En la misma carpeta que el .exe, revisa que exista el archivo `.env`, si no, crea un documento de texto y llamalo exactamente `.env`.
   - Si no existia el archivo .env, copia en el el siguiente contenido:
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

### 1️⃣ Subir Archivos a la Base de Datos
1. Abre la aplicación y selecciona **"Subir Archivos a la Base de Datos"**
2. Elige el tipo de archivo (CSV o PDF) y selecciona el archivo
3. Espera el progreso de carga y confirmación

### 2️⃣ Exportar Datos de un Estudiante a Excel
1. Selecciona **"Exportar Datos de alumno a Excel"**
2. Ingresa el **RUT** del estudiante (sin puntos y con guion)
3. Selecciona las hojas a incluir:
   - ☑️ **Información General**
   - ☑️ **Semestres y Asignaturas**
   - ☑️ **Información Financiera**
   - ☑️ **Notas Media**
   - ☑️ **Hojas Personalizadas**
4. Elige la carpeta de salida
5. Confirma si deseas abrir el archivo al finalizar

### 3️⃣ Exportar Datos por Semestre
1. Selecciona **"Exportar Datos por Semestre"**
2. Elige **Periodo Inicio** y **Periodo Fin**
3. El reporte generará una hoja por cada semestre en el rango
4. Elige la carpeta de salida y confirma si deseas abrir el archivo

### 4️⃣ Exportar Datos Financieros (Morosidad)
1. Selecciona **"Exportar Datos Financieros (Morosidad)"**
2. El reporte incluye solo estudiantes con deuda
3. Se muestra el porcentaje de morosidad y el detalle financiero
4. Elige la carpeta de salida y confirma si deseas abrir el archivo

### 5️⃣ Crear Reporte Personalizado
1. Selecciona **"Crear Hoja Personalizada"**
2. Elige tablas y columnas a incluir
3. Asigna un nombre al reporte y guarda
4. El reporte aparecerá en la lista de hojas personalizadas

### 6️⃣ Eliminar Reporte Personalizado
1. Selecciona **"Borrar Hojas Personalizadas"**
2. Marca los reportes a eliminar y confirma

### 7️⃣ Leer Certificado PDF
1. Selecciona **"Leer Certificado"**
2. Carga el PDF (ANUAL o CONCENTRACIÓN)
3. La aplicación extrae las calificaciones automáticamente

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

### Informacion de contacto:
   - Guillermo Staudt Ossa, +56 9 5001 9329, gastaudt@uc.cl

---

## 🔄 ACTUALIZACIONES

Cuando haya nuevas versiones:
1. Descarga la nueva versión de `Herramienta-Consultas-Inacap.exe`
2. Reemplaza el archivo anterior
3. Mantén tu archivo `.env` en la misma carpeta
4. Tus reportes personalizados se conservarán

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

