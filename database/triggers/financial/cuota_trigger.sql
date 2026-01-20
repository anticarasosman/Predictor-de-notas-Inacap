DROP TRIGGER IF EXISTS cuota_before_update;
DROP TRIGGER IF EXISTS cuota_after_update;
DROP TRIGGER IF EXISTS cuota_before_update_mora;
DELIMITER //

-- Validaciones básicas
CREATE TRIGGER cuota_before_update
BEFORE UPDATE ON Cuota
FOR EACH ROW
BEGIN
    IF NEW.saldo_pendiente < 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: El saldo pendiente no puede ser negativo.';
    END IF;
    IF NEW.fecha_vencimiento < CURDATE() THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: La fecha de vencimiento no puede ser en el pasado.';
    END IF;
END//

-- Ajusta estado según saldo
CREATE TRIGGER cuota_after_update
AFTER UPDATE ON Cuota
FOR EACH ROW
BEGIN
    IF NEW.saldo_pendiente = 0 THEN
        UPDATE Cuota
        SET estado_cuota = 'PAGADO'
        WHERE id_cuota = NEW.id_cuota;
    ELSE
        UPDATE Cuota
        SET estado_cuota = 'PENDIENTE'
        WHERE id_cuota = NEW.id_cuota;
    END IF;
END//

-- Calcula días de mora y marca EN MORA si corresponde
CREATE TRIGGER cuota_before_update_mora
BEFORE UPDATE ON Cuota
FOR EACH ROW
BEGIN
    IF NEW.estado_cuota = 'PENDIENTE' AND NEW.fecha_vencimiento < CURDATE() THEN
        SET NEW.dias_mora = DATEDIFF(CURDATE(), NEW.fecha_vencimiento);
        SET NEW.estado_cuota = 'EN MORA';
    END IF;
END//

DELIMITER ;