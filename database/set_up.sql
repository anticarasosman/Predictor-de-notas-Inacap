-- setup_db.sql
-- Script para crear toda la base de datos

-- Limpiar BD anterior (¡CUIDADO en producción!)
DROP DATABASE IF EXISTS inacap_test;
CREATE DATABASE inacap_test;
USE inacap_test;

-- Crear tablas en orden primero crear tablas core, luego bridge
-- Core tables
SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/schema/core/region.sql;
SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/schema/core/comuna.sql;
SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/schema/core/colegio.sql;
SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/schema/core/estudiante.sql;
SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/schema/core/direccion.sql;

-- Bridge tables
SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/schema/core/historial_institucional.sql;
SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/schema/bridge/estudiante_colegio.sql;
SOURCE c:/Users/gstaudt/Desktop/Predictor-de-notas-Inacap/database/schema/bridge/estudiante_direccion.sql;

-- Insertar datos iniciales
INSERT INTO Region (codigo, nombre) VALUES (11, 'Aysén del General Carlos Ibáñez del Campo');

-- Verificar
SELECT 'Base de datos creada exitosamente!' AS status;
SHOW TABLES;