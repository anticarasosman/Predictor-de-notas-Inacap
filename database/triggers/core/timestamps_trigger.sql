-- ============================================================================
-- TABLA: Múltiples tablas
-- DESCRIPCIÓN: Triggers para actualizar automáticamente fecha_actualizacion
-- ============================================================================
-- Triggers incluidos:
--   1. BEFORE UPDATE en todas las tablas con fecha_actualizacion
--      Actualiza el campo a CURRENT_TIMESTAMP
-- ============================================================================

-- ============================================================================
-- AREA_ACADEMICA - UPDATE TIMESTAMP
-- ============================================================================
DROP TRIGGER IF EXISTS tr_area_academica_update;
DELIMITER //
CREATE TRIGGER tr_area_academica_update
BEFORE UPDATE ON Area_Academica
FOR EACH ROW
BEGIN
    SET NEW.fecha_actualizacion = CURRENT_TIMESTAMP;
END//
DELIMITER ;

-- ============================================================================
-- AREA_CONOCIMIENTO - UPDATE TIMESTAMP
-- ============================================================================
DROP TRIGGER IF EXISTS tr_area_conocimiento_update;
DELIMITER //
CREATE TRIGGER tr_area_conocimiento_update
BEFORE UPDATE ON Area_Conocimiento
FOR EACH ROW
BEGIN
    SET NEW.fecha_actualizacion = CURRENT_TIMESTAMP;
END//
DELIMITER ;

-- ============================================================================
-- CARRERA - UPDATE TIMESTAMP
-- ============================================================================
DROP TRIGGER IF EXISTS tr_carrera_update;
DELIMITER //
CREATE TRIGGER tr_carrera_update
BEFORE UPDATE ON Carrera
FOR EACH ROW
BEGIN
    SET NEW.fecha_actualizacion = CURRENT_TIMESTAMP;
END//
DELIMITER ;

-- ============================================================================
-- COLEGIO - UPDATE TIMESTAMP
-- ============================================================================
DROP TRIGGER IF EXISTS tr_colegio_update;
DELIMITER //
CREATE TRIGGER tr_colegio_update
BEFORE UPDATE ON Colegio
FOR EACH ROW
BEGIN
    SET NEW.fecha_actualizacion = CURRENT_TIMESTAMP;
END//
DELIMITER ;

-- ============================================================================
-- COMUNA - UPDATE TIMESTAMP
-- ============================================================================
DROP TRIGGER IF EXISTS tr_comuna_update;
DELIMITER //
CREATE TRIGGER tr_comuna_update
BEFORE UPDATE ON Comuna
FOR EACH ROW
BEGIN
    SET NEW.fecha_actualizacion = CURRENT_TIMESTAMP;
END//
DELIMITER ;

-- ============================================================================
-- CUOTA - UPDATE TIMESTAMP
-- ============================================================================
DROP TRIGGER IF EXISTS tr_cuota_update;
DELIMITER //
CREATE TRIGGER tr_cuota_update
BEFORE UPDATE ON Cuota
FOR EACH ROW
BEGIN
    SET NEW.fecha_actualizacion = CURRENT_TIMESTAMP;
END//
DELIMITER ;

-- ============================================================================
-- DIRECCION - UPDATE TIMESTAMP
-- ============================================================================
DROP TRIGGER IF EXISTS tr_direccion_update;
DELIMITER //
CREATE TRIGGER tr_direccion_update
BEFORE UPDATE ON Direccion
FOR EACH ROW
BEGIN
    SET NEW.fecha_actualizacion = CURRENT_TIMESTAMP;
END//
DELIMITER ;

-- ============================================================================
-- ESTUDIANTE - UPDATE TIMESTAMP
-- ============================================================================
DROP TRIGGER IF EXISTS tr_estudiante_update;
DELIMITER //
CREATE TRIGGER tr_estudiante_update
BEFORE UPDATE ON Estudiante
FOR EACH ROW
BEGIN
    SET NEW.fecha_actualizacion = CURRENT_TIMESTAMP;
END//
DELIMITER ;

-- ============================================================================
-- HISTORIAL_INSTITUCIONAL - UPDATE TIMESTAMP
-- ============================================================================
DROP TRIGGER IF EXISTS tr_historial_institucional_update;
DELIMITER //
CREATE TRIGGER tr_historial_institucional_update
BEFORE UPDATE ON HistorialInstitucional
FOR EACH ROW
BEGIN
    SET NEW.fecha_actualizacion = CURRENT_TIMESTAMP;
END//
DELIMITER ;

-- ============================================================================
-- INSCRIPCIONES_RAMOS - UPDATE TIMESTAMP
-- ============================================================================
DROP TRIGGER IF EXISTS tr_inscripciones_ramos_update;
DELIMITER //
CREATE TRIGGER tr_inscripciones_ramos_update
BEFORE UPDATE ON Inscripciones_Ramos
FOR EACH ROW
BEGIN
    SET NEW.fecha_actualizacion = CURRENT_TIMESTAMP;
END//
DELIMITER ;

-- ============================================================================
-- INSTITUCION - UPDATE TIMESTAMP
-- ============================================================================
DROP TRIGGER IF EXISTS tr_institucion_update;
DELIMITER //
CREATE TRIGGER tr_institucion_update
BEFORE UPDATE ON Institucion
FOR EACH ROW
BEGIN
    SET NEW.fecha_actualizacion = CURRENT_TIMESTAMP;
END//
DELIMITER ;

-- ============================================================================
-- MATRICULA - UPDATE TIMESTAMP
-- ============================================================================
DROP TRIGGER IF EXISTS tr_matricula_update;
DELIMITER //
CREATE TRIGGER tr_matricula_update
BEFORE UPDATE ON Matricula
FOR EACH ROW
BEGIN
    SET NEW.fecha_actualizacion = CURRENT_TIMESTAMP;
END//
DELIMITER ;

-- ============================================================================
-- NOTAS_ESTUDIANTE - UPDATE TIMESTAMP
-- ============================================================================
DROP TRIGGER IF EXISTS tr_notas_estudiante_update;
DELIMITER //
CREATE TRIGGER tr_notas_estudiante_update
BEFORE UPDATE ON Notas_Estudiante
FOR EACH ROW
BEGIN
    SET NEW.fecha_actualizacion = CURRENT_TIMESTAMP;
END//
DELIMITER ;

-- ============================================================================
-- PAGO - UPDATE TIMESTAMP
-- ============================================================================
DROP TRIGGER IF EXISTS tr_pago_update;
DELIMITER //
CREATE TRIGGER tr_pago_update
BEFORE UPDATE ON Pago
FOR EACH ROW
BEGIN
    SET NEW.fecha_actualizacion = CURRENT_TIMESTAMP;
END//
DELIMITER ;

-- ============================================================================
-- PLAN_ESTUDIO - UPDATE TIMESTAMP
-- ============================================================================
DROP TRIGGER IF EXISTS tr_plan_estudio_update;
DELIMITER //
CREATE TRIGGER tr_plan_estudio_update
BEFORE UPDATE ON Plan_Estudio
FOR EACH ROW
BEGIN
    SET NEW.fecha_actualizacion = CURRENT_TIMESTAMP;
END//
DELIMITER ;

-- ============================================================================
-- PREDICTOR_DATOS - UPDATE TIMESTAMP
-- ============================================================================
DROP TRIGGER IF EXISTS tr_predictor_datos_update;
DELIMITER //
CREATE TRIGGER tr_predictor_datos_update
BEFORE UPDATE ON Predictor_Datos
FOR EACH ROW
BEGIN
    SET NEW.fecha_actualizacion = CURRENT_TIMESTAMP;
END//
DELIMITER ;

-- ============================================================================
-- PREREQUISITOS - UPDATE TIMESTAMP
-- ============================================================================
DROP TRIGGER IF EXISTS tr_prerequisitos_update;
DELIMITER //
CREATE TRIGGER tr_prerequisitos_update
BEFORE UPDATE ON PREREQUISITOS
FOR EACH ROW
BEGIN
    SET NEW.fecha_actualizacion = CURRENT_TIMESTAMP;
END//
DELIMITER ;

-- ============================================================================
-- PROFESOR - UPDATE TIMESTAMP
-- ============================================================================
DROP TRIGGER IF EXISTS tr_profesor_update;
DELIMITER //
CREATE TRIGGER tr_profesor_update
BEFORE UPDATE ON Profesor
FOR EACH ROW
BEGIN
    SET NEW.fecha_actualizacion = CURRENT_TIMESTAMP;
END//
DELIMITER ;

-- ============================================================================
-- RAMO - UPDATE TIMESTAMP
-- ============================================================================
DROP TRIGGER IF EXISTS tr_ramo_update;
DELIMITER //
CREATE TRIGGER tr_ramo_update
BEFORE UPDATE ON Ramo
FOR EACH ROW
BEGIN
    SET NEW.fecha_actualizacion = CURRENT_TIMESTAMP;
END//
DELIMITER ;

-- ============================================================================
-- RAMOS_PLAN_ESTUDIO - UPDATE TIMESTAMP
-- ============================================================================
DROP TRIGGER IF EXISTS tr_ramos_plan_estudio_update;
DELIMITER //
CREATE TRIGGER tr_ramos_plan_estudio_update
BEFORE UPDATE ON Ramos_Plan_Estudio
FOR EACH ROW
BEGIN
    SET NEW.fecha_actualizacion = CURRENT_TIMESTAMP;
END//
DELIMITER ;

-- ============================================================================
-- REGION - UPDATE TIMESTAMP
-- ============================================================================
DROP TRIGGER IF EXISTS tr_region_update;
DELIMITER //
CREATE TRIGGER tr_region_update
BEFORE UPDATE ON Region
FOR EACH ROW
BEGIN
    SET NEW.fecha_actualizacion = CURRENT_TIMESTAMP;
END//
DELIMITER ;

-- ============================================================================
-- SECCIONES_RAMOS - UPDATE TIMESTAMP
-- ============================================================================
DROP TRIGGER IF EXISTS tr_secciones_ramos_update;
DELIMITER //
CREATE TRIGGER tr_secciones_ramos_update
BEFORE UPDATE ON Secciones_Ramos
FOR EACH ROW
BEGIN
    SET NEW.fecha_actualizacion = CURRENT_TIMESTAMP;
END//
DELIMITER ;

-- ============================================================================
-- TRANSACCION_PAGO - UPDATE TIMESTAMP
-- ============================================================================
DROP TRIGGER IF EXISTS tr_transaccion_pago_update;
DELIMITER //
CREATE TRIGGER tr_transaccion_pago_update
BEFORE UPDATE ON Transaccion_Pago
FOR EACH ROW
BEGIN
    SET NEW.fecha_actualizacion = CURRENT_TIMESTAMP;
END//
DELIMITER ;