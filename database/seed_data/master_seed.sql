-- ======================================================
-- MASTER SEED DATA - Carga de datos iniciales para testing
-- Base de datos: inacap_test
-- ======================================================
-- Este script carga datos semilla en todas las tablas
-- para facilitar el testing sin necesidad de insertar
-- manualmente datos de prueba cada vez.
-- ======================================================

USE inacap_test;

-- Deshabilitar verificación de claves foráneas temporalmente
SET FOREIGN_KEY_CHECKS = 0;

-- ======================================================
-- FASE 1: Tablas base (sin dependencias)
-- ======================================================

SOURCE 01_region.sql;
SOURCE 02_area_academica.sql;
SOURCE 03_area_conocimiento.sql;
SOURCE 04_institucion.sql;

-- ======================================================
-- FASE 2: Tablas con una dependencia
-- ======================================================

SOURCE 05_comuna.sql;
SOURCE 06_direccion.sql;
SOURCE 07_ramo.sql;
SOURCE 08_profesor.sql;

-- ======================================================
-- FASE 3: Tablas con dependencias compuestas
-- ======================================================

SOURCE 09_colegio.sql;
SOURCE 10_estudiante.sql;
SOURCE 11_plan_estudio.sql;
SOURCE 12_carrera.sql;
SOURCE 13_historial_institucional.sql;
SOURCE 14_prerequisitos.sql;
SOURCE 15_ramos_plan_estudio.sql;
SOURCE 16_secciones_ramos.sql;

-- ======================================================
-- FASE 4: Tablas con dependencias circulares
-- (Requieren orden específico)
-- ======================================================

-- IMPORTANTE: Predictor_Datos y Matricula tienen dependencia circular
-- Se debe insertar Matricula primero con id_predictor_datos NULL o ajustar schema

-- Opción 1: Insertar Predictor_Datos sin id_matricula (si el schema lo permite)
-- Opción 2: Modificar Matricula para permitir NULL en id_predictor_datos

SOURCE 18_matricula.sql;
SOURCE 17_predictor_datos.sql;

-- ======================================================
-- FASE 5: Tablas de gestión académica y financiera
-- ======================================================

SOURCE 19_notas_estudiante.sql;
SOURCE 20_inscripciones_ramos.sql;
SOURCE 21_pagos.sql;
SOURCE 22_cuota.sql;
SOURCE 23_transaccion_pago.sql;

-- ======================================================
-- FASE 6: Tablas puente (relaciones many-to-many)
-- ======================================================

SOURCE 24_estudiante_colegio.sql;
SOURCE 25_estudiante_direccion.sql;
SOURCE 26_ramo_areaConocimiento.sql;
SOURCE 27_ramosPlanEstudio_prerequisito.sql;

-- Rehabilitar verificación de claves foráneas
SET FOREIGN_KEY_CHECKS = 1;

-- ======================================================
-- Verificación de datos cargados
-- ======================================================

SELECT 'DATOS SEMILLA CARGADOS EXITOSAMENTE' AS RESULTADO;

SELECT 
    'Region' AS Tabla, COUNT(*) AS Registros FROM Region
UNION ALL
SELECT 'Comuna', COUNT(*) FROM Comuna
UNION ALL
SELECT 'Direccion', COUNT(*) FROM Direccion
UNION ALL
SELECT 'Area_Academica', COUNT(*) FROM Area_Academica
UNION ALL
SELECT 'Area_Conocimiento', COUNT(*) FROM Area_Conocimiento
UNION ALL
SELECT 'Institucion', COUNT(*) FROM Institucion
UNION ALL
SELECT 'Colegio', COUNT(*) FROM Colegio
UNION ALL
SELECT 'Estudiante', COUNT(*) FROM Estudiante
UNION ALL
SELECT 'Profesor', COUNT(*) FROM Profesor
UNION ALL
SELECT 'Ramo', COUNT(*) FROM Ramo
UNION ALL
SELECT 'Plan_Estudio', COUNT(*) FROM Plan_Estudio
UNION ALL
SELECT 'Carrera', COUNT(*) FROM Carrera
UNION ALL
SELECT 'Matricula', COUNT(*) FROM Matricula
UNION ALL
SELECT 'Notas_Estudiante', COUNT(*) FROM Notas_Estudiante
UNION ALL
SELECT 'Inscripciones_Ramos', COUNT(*) FROM Inscripciones_Ramos
UNION ALL
SELECT 'estudiante_colegio', COUNT(*) FROM estudiante_colegio
UNION ALL
SELECT 'estudiante_direccion', COUNT(*) FROM estudiante_direccion;

-- ======================================================
-- FIN DEL SCRIPT MAESTRO
-- ======================================================
