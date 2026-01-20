DROP TRIGGER IF EXISTS inscripciones_ramos_before_update;
DROP TRIGGER IF EXISTS inscripciones_ramos_after_update;
DELIMITER $$

CREATE TRIGGER inscripciones_ramos_before_update
BEFORE UPDATE ON Inscripciones_Ramos
FOR EACH ROW
BEGIN
    IF NEW.nota_final >= 4.0 THEN
        SET NEW.situacion_final = 'APROBADO';
    ELSE
        SET NEW.situacion_final = 'REPROBADO';
    END IF;
END$$

CREATE TRIGGER inscripciones_ramos_after_update
AFTER UPDATE ON Inscripciones_Ramos
FOR EACH ROW
BEGIN
    DECLARE v_id_matricula INT;
    
    -- Obtener la matrícula del estudiante para el semestre correspondiente
    SELECT m.id_matricula INTO v_id_matricula
    FROM Matricula m
    WHERE m.id_estudiante = NEW.id_estudiante
    ORDER BY m.fecha_matricula DESC
    LIMIT 1;
    
    -- Si el tipo cambió a CONVALIDACION (y antes no lo era) y está aprobado
    IF NEW.tipo_inscripcion = 'CONVALIDACION' 
       AND OLD.tipo_inscripcion != 'CONVALIDACION' 
       AND NEW.situacion_final = 'APROBADO'
       AND v_id_matricula IS NOT NULL THEN
        UPDATE Matricula
        SET numero_de_convalidaciones = numero_de_convalidaciones + 1
        WHERE id_matricula = v_id_matricula;
    END IF;
    
    -- Si el tipo cambió a HOMOLOGACION (y antes no lo era) y está aprobado
    IF NEW.tipo_inscripcion = 'HOMOLOGACION' 
       AND OLD.tipo_inscripcion != 'HOMOLOGACION' 
       AND NEW.situacion_final = 'APROBADO'
       AND v_id_matricula IS NOT NULL THEN
        UPDATE Matricula
        SET numero_de_homologaciones = numero_de_homologaciones + 1
        WHERE id_matricula = v_id_matricula;
    END IF;
END$$

DELIMITER ;