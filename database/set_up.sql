-- setup_db.sql
-- Script para crear toda la base de datos

-- Limpiar BD anterior (¡CUIDADO en producción!)
DROP DATABASE IF EXISTS inacap_test;
CREATE DATABASE inacap_test;
USE inacap_test;

-- Crear tablas en orden correcto (respetando dependencias de Foreign Keys)

-- FASE 1: Tablas base sin dependencias
SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/schema/core/estudiante.sql;
SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/schema/core/semestre.sql;
SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/schema/core/asignatura.sql;

SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/schema/core/reporte_financiero_estudiante.sql;

SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/schema/bridge/estudiante_semestre.sql;
SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/schema/bridge/asignatura_semestre.sql;

-- ======================================================
-- CARGAR DATOS SEMILLA (SEED DATA)
-- ======================================================

SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/seed_data/01_estudiante.sql;
SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/seed_data/02_semestre.sql;
SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/seed_data/03_asignatura.sql;

SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/seed_data/04_reporte_financiero_estudiante.sql;

SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/seed_data/05_estudiante_semestre.sql;
SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/seed_data/06_asignatura_semestre.sql;

-- ============================================================================
-- CARGA DE TRIGGERS
-- ============================================================================
-- SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/triggers/init_triggers.sql;

-- Verificar
SELECT 'Base de datos creada exitosamente!' AS status;
SHOW TABLES;