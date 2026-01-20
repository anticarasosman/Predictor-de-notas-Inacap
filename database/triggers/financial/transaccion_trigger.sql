DROP TRIGGER IF EXISTS transaccion_before_insert;
DROP TRIGGER IF EXISTS transaccion_before_update;
DROP TRIGGER IF EXISTS transaccion_after_insert;
DELIMITER $$

CREATE TRIGGER transaccion_before_insert
BEFORE INSERT ON Transaccion
FOR EACH ROW
BEGIN
    DECLARE pago_estudiante INT;
    DECLARE cuota_pago INT;
    DECLARE cuota_estudiante INT;
    
    -- Validación 1: monto debe ser > 0
    IF NEW.monto_transaccion <= 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'El monto de la transacción debe ser mayor que cero.';
    END IF;
    
    -- Validación 2: Si tipo es PAGO, verificar que pertenece al estudiante
    IF NEW.tipo_transaccion = 'PAGO' THEN
        SELECT m.id_estudiante INTO pago_estudiante
        FROM Pago p
        JOIN Matricula m ON p.id_matricula = m.id_matricula
        WHERE p.id_pago = NEW.id_pago;
        
        IF pago_estudiante IS NULL OR pago_estudiante != NEW.id_estudiante THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'El Pago no pertenece al estudiante de esta transacción.';
        END IF;
    END IF;
    
    -- Validación 3: Si tipo es CUOTA, verificar que pertenece al estudiante
    IF NEW.tipo_transaccion = 'CUOTA' THEN
        SELECT p.id_pago INTO cuota_pago
        FROM Cuota WHERE id_cuota = NEW.id_cuota;
        
        IF cuota_pago IS NULL THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'La Cuota especificada no existe.';
        END IF;
        
        SELECT m.id_estudiante INTO cuota_estudiante
        FROM Pago p
        JOIN Matricula m ON p.id_matricula = m.id_matricula
        WHERE p.id_pago = cuota_pago;
        
        IF cuota_estudiante IS NULL OR cuota_estudiante != NEW.id_estudiante THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'La Cuota no pertenece al estudiante de esta transacción.';
        END IF;
    END IF;
END$$

CREATE TRIGGER transaccion_after_insert
AFTER INSERT ON Transaccion
FOR EACH ROW
BEGIN
    -- Si el tipo es PAGO, actualizar tabla Pago
    IF NEW.tipo_transaccion = 'PAGO' THEN
        UPDATE Pago
        SET 
            monto_pagado = monto_pagado + NEW.monto_transaccion,
            fecha_pago = CURDATE(),
            estado_pago = CASE
                WHEN (monto_pagado + NEW.monto_transaccion) >= monto_total THEN 'PAGADO'
                WHEN CURDATE() > fecha_vencimiento THEN 'EN MORA'
                WHEN CURDATE() = fecha_vencimiento THEN 'VENCIDO'
                ELSE 'PENDIENTE'
            END,
            fecha_registro_pago = CURDATE(),
            fecha_actualizacion = CURRENT_TIMESTAMP
        WHERE id_pago = NEW.id_pago;
    END IF;
    
    -- Si el tipo es CUOTA, actualizar tabla Cuota
    IF NEW.tipo_transaccion = 'CUOTA' THEN
        UPDATE Cuota
        SET 
            monto_pagado = monto_pagado + NEW.monto_transaccion,
            fecha_pago = CURDATE(),
            estado_cuota = CASE
                WHEN (monto_pagado + NEW.monto_transaccion) >= monto_cuota THEN 'PAGADO'
                WHEN CURDATE() > fecha_vencimiento THEN 'EN MORA'
                WHEN CURDATE() = fecha_vencimiento THEN 'VENCIDO'
                ELSE 'PENDIENTE'
            END,
            fecha_registro_pago = CURDATE(),
            fecha_actualizacion = CURRENT_TIMESTAMP
        WHERE id_cuota = NEW.id_cuota;
    END IF;
END$$

DELIMITER ;