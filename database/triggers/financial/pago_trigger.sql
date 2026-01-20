DROP TRIGGER IF EXISTS pago_before_insert;
DELIMITER //
CREATE TRIGGER pago_before_insert
BEFORE INSERT ON Pago
FOR EACH ROW
BEGIN
    IF NEW.monto_pagado < 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: El monto pagado no puede ser negativo.';
    END IF;
    IF NEW.fecha_pago > CURDATE() THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: La fecha de pago no puede ser futura.';
    END IF;
    IF NEW.monto_pagado > NEW.monto_total THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: El monto pagado no puede ser mayor que el monto total.';
    END IF;
END;
//