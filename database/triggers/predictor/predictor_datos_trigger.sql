DROP TRIGGER IF EXISTS predictor_datos_before_insert;
DROP TRIGGER IF EXISTS predictor_datos_before_update;
DELIMITER $$

CREATE TRIGGER predictor_datos_before_insert
BEFORE INSERT ON Predictor_Datos
FOR EACH ROW
BEGIN
    -- Validar formato de semestre_evaluacion (YYYY-X donde X es 1 o 2)
    IF NEW.semestre_evaluacion IS NOT NULL 
       AND NEW.semestre_evaluacion NOT REGEXP '^[0-9]{4}-[12]$' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'El formato de semestre_evaluacion debe ser YYYY-X (ejemplo: 2025-1 o 2025-2).';
    END IF;
    
    -- Validar que logro_porcentaje esté entre 0 y 100
    IF NEW.logro_porcentaje IS NOT NULL 
       AND (NEW.logro_porcentaje < 0 OR NEW.logro_porcentaje > 100) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'El logro_porcentaje debe estar entre 0 y 100.';
    END IF;
END$$

CREATE TRIGGER predictor_datos_before_update
BEFORE UPDATE ON Predictor_Datos
FOR EACH ROW
BEGIN
    -- Validar formato de semestre_evaluacion (YYYY-X donde X es 1 o 2)
    IF NEW.semestre_evaluacion IS NOT NULL 
       AND NEW.semestre_evaluacion NOT REGEXP '^[0-9]{4}-[12]$' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'El formato de semestre_evaluacion debe ser YYYY-X (ejemplo: 2025-1 o 2025-2).';
    END IF;
    
    -- Validar que logro_porcentaje esté entre 0 y 100
    IF NEW.logro_porcentaje IS NOT NULL 
       AND (NEW.logro_porcentaje < 0 OR NEW.logro_porcentaje > 100) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'El logro_porcentaje debe estar entre 0 y 100.';
    END IF;
END$$

DELIMITER ;
