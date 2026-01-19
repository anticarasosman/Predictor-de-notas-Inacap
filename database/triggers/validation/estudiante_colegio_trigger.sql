DROP TRIGGER IF EXISTS estudiando_colegio_before_insert;
DELIMITER //
CREATE TRIGGER estudiando_colegio_before_insert
BEFORE INSERT ON Estudiante_Colegio
FOR EACH ROW
BEGIN
    IF NEW.ano_inicio > NEW.ano_fin THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'El año de inicio no puede ser mayor que el año de fin.';
    END IF;
END;
//
DELIMITER ;

DROP TRIGGER IF EXISTS estudiando_colegio_before_update;
DELIMITER //
CREATE TRIGGER estudiando_colegio_before_update
BEFORE UPDATE ON Estudiante_Colegio
FOR EACH ROW
BEGIN
    IF NEW.ano_inicio > NEW.ano_fin THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'El año de inicio no puede ser mayor que el año de fin.';
    END IF;
END;
//
DELIMITER ;