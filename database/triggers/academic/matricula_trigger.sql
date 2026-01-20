DROP TRIGGER IF EXISTS matricula_before_insert;
DELIMITER //

CREATE TRIGGER matricula_before_insert
BEFORE INSERT ON Matricula
FOR EACH ROW
BEGIN
    IF NEW.ultimo_semestre_cursado < NEW.semestre_ingreso THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'El último semestre cursado no puede ser anterior al semestre de ingreso.';
    END IF;
END;
//
DELIMITER ;

DROP TRIGGER IF EXISTS matricula_before_update;
CREATE TRIGGER matricula_before_update
BEFORE UPDATE ON Matricula
FOR EACH ROW
BEGIN
    IF NEW.ultimo_semestre_cursado < NEW.semestre_ingreso THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'El último semestre cursado no puede ser anterior al semestre de ingreso.';
    END IF;
END;
//
DELIMITER ;
