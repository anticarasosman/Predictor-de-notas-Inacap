-- setup_db.sql
-- Script para crear toda la base de datos

-- Limpiar BD anterior (¡CUIDADO en producción!)
DROP DATABASE IF EXISTS inacap_test;
CREATE DATABASE inacap_test;
USE inacap_test;

-- Crear tablas en orden correcto (respetando dependencias de Foreign Keys)

-- FASE 1: Tablas base sin dependencias
SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/schema/core/region.sql;
SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/schema/core/area_academica.sql;
SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/schema/core/area_conocimiento.sql;
SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/schema/core/institucion.sql;
SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/schema/core/profesor.sql;
SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/schema/core/estudiante.sql;
SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/schema/core/ramo.sql;

-- FASE 2: Tablas con 1 nivel de dependencia
SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/schema/core/comuna.sql;
SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/schema/core/prerequisitos.sql;
SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/schema/core/historial_institucional.sql;
SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/schema/core/notas_estudiante.sql;

-- FASE 3: Tablas con 2 niveles de dependencia
SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/schema/core/direccion.sql;
SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/schema/core/colegio.sql;
SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/schema/core/planes_estudio.sql;
SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/schema/core/ramos_plan_estudio.sql;
SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/schema/core/secciones_ramos.sql;

-- FASE 4: Tablas con múltiples dependencias
SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/schema/core/carrera.sql;

-- FASE 5: Dependencias circulares (Matricula y Predictor_Datos)
-- Nota: Si hay dependencia circular, ajustar uno de los campos a NULL o crear sin FK primero
SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/schema/core/matricula.sql;
SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/schema/core/predictor_datos.sql;

-- FASE 6: Gestión financiera
SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/schema/core/pago.sql;
SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/schema/core/cuota.sql;
SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/schema/core/transaccion_pago.sql;

-- FASE 7: Inscripciones (dependen de casi todo)
SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/schema/core/inscripciones_ramos.sql;

-- FASE 8: Tablas puente (relaciones many-to-many)
SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/schema/bridge/estudiante_colegio.sql;
SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/schema/bridge/estudiante_direccion.sql;
SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/schema/bridge/ramo_areaConocimiento.sql;
SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/schema/bridge/ramosPlanEstudio_prerequisito.sql;

-- ======================================================
-- CARGAR DATOS SEMILLA (SEED DATA)
-- ======================================================

-- FASE 1: Tablas base
SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/seed_data/01_region.sql;
SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/seed_data/02_area_academica.sql;
SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/seed_data/03_area_conocimiento.sql;
SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/seed_data/04_institucion.sql;

-- FASE 2: Tablas con 1 dependencia
SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/seed_data/05_comuna.sql;
SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/seed_data/06_direccion.sql;
SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/seed_data/07_ramo.sql;
SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/seed_data/08_profesor.sql;

-- FASE 3: Tablas con 2 dependencias
SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/seed_data/09_colegio.sql;
SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/seed_data/10_estudiante.sql;
SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/seed_data/11_plan_estudio.sql;
SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/seed_data/12_carrera.sql;
SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/seed_data/13_historial_institucional.sql;
SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/seed_data/14_prerequisitos.sql;
SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/seed_data/15_ramos_plan_estudio.sql;
SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/seed_data/16_secciones_ramos.sql;

-- FASE 4: Dependencias circulares
SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/seed_data/18_matricula.sql;
SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/seed_data/17_predictor_datos.sql;

-- FASE 5: Gestión académica y financiera
SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/seed_data/19_notas_estudiante.sql;
SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/seed_data/20_inscripciones_ramos.sql;
SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/seed_data/21_pagos.sql;
SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/seed_data/22_cuota.sql;
SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/seed_data/23_transaccion_pago.sql;

-- FASE 6: Tablas puente (relaciones many-to-many)
SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/seed_data/24_estudiante_colegio.sql;
SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/seed_data/25_estudiante_direccion.sql;
SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/seed_data/26_ramo_areaConocimiento.sql;
SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/seed_data/27_ramosPlanEstudio_prerequisito.sql;

-- Verificar
SELECT 'Base de datos creada exitosamente!' AS status;
SHOW TABLES;