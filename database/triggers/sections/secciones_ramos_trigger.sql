DROP TRIGGER IF EXISTS secciones_ramos_before_update;
DELIMITER //
CREATE TRIGGER secciones_ramos_before_update
AFTER UPDATE ON Secciones_Ramos
FOR EACH ROW
BEGIN
    IF NEW.cupos_ocupados > OLD.cupos_totales THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: Los cupos ocupados no pueden ser mayores que los cupos totales.';
    END IF;
END//
DELIMITER ;