DROP TRIGGER IF EXISTS ramos_plan_estudio_after_update;
DELIMITER //
CREATE TRIGGER ramos_plan_estudio_after_update
AFTER UPDATE ON Ramo
FOR EACH ROW 
BEGIN
    IF OLD.activo = TRUE AND NEW.activo = FALSE THEN
        UPDATE Ramos_Plan_Estudio rpe
        INNER JOIN Ramos_Plan_Estudio_Ramo rper 
            ON rpe.id_ramo_plan_estudio = rper.id_ramo_plan_estudio
        SET rpe.activo_en_plan = FALSE
        WHERE rper.id_ramo = OLD.id_ramo;
    END IF;
END;
//
DELIMITER ;