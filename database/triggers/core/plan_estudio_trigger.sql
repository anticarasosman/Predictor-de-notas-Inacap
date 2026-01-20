DROP TRIGGER IF EXISTS plan_estudio_before_insert;
DROP TRIGGER IF EXISTS plan_estudio_before_update;
DELIMITER $$

CREATE TRIGGER plan_estudio_before_insert
BEFORE INSERT ON Plan_Estudio
FOR EACH ROW
BEGIN
    -- Validar que duracion_estimada_semestres sea mayor que 0
    IF NEW.duracion_estimada_semestres <= 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'La duración estimada en semestres debe ser mayor que 0.';
    END IF;
    
    -- Validar que fecha_inicio <= fecha_fin (si fecha_fin no es NULL)
    IF NEW.fecha_fin IS NOT NULL AND NEW.fecha_inicio > NEW.fecha_fin THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'La fecha de inicio no puede ser posterior a la fecha de fin.';
    END IF;
END$$

CREATE TRIGGER plan_estudio_before_update
BEFORE UPDATE ON Plan_Estudio
FOR EACH ROW
BEGIN
    -- Validar que duracion_estimada_semestres sea mayor que 0
    IF NEW.duracion_estimada_semestres <= 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'La duración estimada en semestres debe ser mayor que 0.';
    END IF;
    
    -- Validar que fecha_inicio <= fecha_fin (si fecha_fin no es NULL)
    IF NEW.fecha_fin IS NOT NULL AND NEW.fecha_inicio > NEW.fecha_fin THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'La fecha de inicio no puede ser posterior a la fecha de fin.';
    END IF;
END$$

DELIMITER ;
