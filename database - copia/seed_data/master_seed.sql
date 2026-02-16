-- ======================================================
-- MASTER SEED DATA - Carga de datos iniciales para testing
-- Base de datos: inacap_test
-- ======================================================

USE inacap_test;

-- Configurar charset para esta sesión
SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;

-- Deshabilitar verificación de claves foráneas temporalmente
SET FOREIGN_KEY_CHECKS = 0;

-- Limpieza previa (orden inverso de dependencias)
TRUNCATE TABLE Estudiante_Asignatura;
TRUNCATE TABLE Asignatura_Semestre;
TRUNCATE TABLE Estudiante_Semestre;
TRUNCATE TABLE Reporte_Financiero_Estudiante;
TRUNCATE TABLE Asignatura;
TRUNCATE TABLE Semestre;
TRUNCATE TABLE Estudiante;

-- ======================================================
-- Carga de datos semilla (orden por dependencias)
-- ======================================================

SOURCE 01_estudiante.sql;
SOURCE 02_semestre.sql;
SOURCE 03_asignatura.sql;
SOURCE 04_reporte_financiero.sql;
SOURCE 05_estudiante_semestre.sql;
SOURCE 06_asignatura_semestre.sql;
SOURCE 07_estudiante_asignatura.sql;

-- Rehabilitar verificación de claves foráneas
SET FOREIGN_KEY_CHECKS = 1;

-- Verificación rápida
SELECT 'DATOS SEMILLA CARGADOS EXITOSAMENTE' AS RESULTADO;
SELECT 'Estudiante' AS Tabla, COUNT(*) AS Registros FROM Estudiante
UNION ALL
SELECT 'Semestre', COUNT(*) FROM Semestre
UNION ALL
SELECT 'Asignatura', COUNT(*) FROM Asignatura
UNION ALL
SELECT 'Reporte_financiero_estudiante', COUNT(*) FROM Reporte_financiero_estudiante
UNION ALL
SELECT 'Estudiante_semestre', COUNT(*) FROM Estudiante_Semestre
UNION ALL
SELECT 'Asignatura_semestre', COUNT(*) FROM Asignatura_Semestre
UNION ALL
SELECT 'Estudiante_asignatura', COUNT(*) FROM Estudiante_Asignatura;

-- ======================================================
-- FIN DEL SCRIPT MAESTRO
-- ======================================================
