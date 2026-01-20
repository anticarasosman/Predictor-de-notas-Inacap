DROP TRIGGER IF EXISTS profesor_before_insert;
DELIMITER //
CREATE TRIGGER profesor_before_insert
BEFORE INSERT ON Profesor
FOR EACH ROW
BEGIN
    IF NEW.fecha_nacimiento IS NOT NULL THEN
        SET NEW.edad = TIMESTAMPDIFF(YEAR, NEW.fecha_nacimiento, CURDATE());
    ELSE
        SET NEW.edad = NULL;
    END IF;
END;
//
DELIMITER ;