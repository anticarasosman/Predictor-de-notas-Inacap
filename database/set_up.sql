-- setup_db.sql
-- Script para crear toda la base de datos

-- Limpiar BD anterior (¡CUIDADO en producción!)
DROP DATABASE IF EXISTS inacap_test;
CREATE DATABASE inacap_test;
USE inacap_test;

-- Crear tablas en orden correcto (respetando dependencias de Foreign Keys)

-- FASE 1: Tablas base sin dependencias
SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/schema/core/estudiante.sql;
SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/schema/core/ramo.sql;

-- FASE 2: Tablas con 1 nivel de dependencia
SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/schema/core/prerequisitos.sql;
SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/schema/core/notas_estudiante.sql;

-- FASE 3: Tablas con 2 niveles de dependencia
SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/schema/core/planes_estudio.sql;
SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/schema/core/ramos_plan_estudio.sql;

-- FASE 4: Gestión financiera
SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/schema/core/cuota.sql;

-- FASE 5: Inscripciones (dependen de casi todo)
SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/schema/core/inscripciones_ramos.sql;

-- FASE 6: Tablas puente (relaciones many-to-many)
SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/schema/bridge/estudiante_colegio.sql;
SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/schema/bridge/estudiante_direccion.sql;
SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/schema/bridge/ramo_areaConocimiento.sql;
SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/schema/bridge/ramosPlanEstudio_prerequisito.sql;

-- ======================================================
-- CARGAR DATOS SEMILLA (SEED DATA)
-- ======================================================

SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/seed_data/07_ramo.sql;

-- FASE 3: Tablas con 2 dependencias
SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/seed_data/10_estudiante.sql;
SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/seed_data/11_plan_estudio.sql;
SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/seed_data/14_prerequisitos.sql;

-- FASE 4: Gestión académica y financiera
SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/seed_data/19_notas_estudiante.sql;
SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/seed_data/20_inscripciones_ramos.sql;

-- FASE 5: Tablas puente (relaciones many-to-many)
SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/seed_data/26_ramo_areaConocimiento.sql;
SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/seed_data/27_ramosPlanEstudio_prerequisito.sql;

-- ============================================================================
-- CARGA DE TRIGGERS
-- ============================================================================
SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/triggers/init_triggers.sql;

-- Verificar
SELECT 'Base de datos creada exitosamente!' AS status;
SHOW TABLES;