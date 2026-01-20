DROP TRIGGER IF EXISTS notas_estudiante_bi;
DROP TRIGGER IF EXISTS notas_estudiante_bu;
DELIMITER $$

CREATE TRIGGER notas_estudiante_bi
BEFORE INSERT ON Notas_Estudiante
FOR EACH ROW
BEGIN
    SET NEW.rendimiento_matematicas = CASE
        WHEN NEW.promedio_matematicas IS NULL THEN NULL
        WHEN NEW.promedio_matematicas < 4.0 THEN 'EN RIESGO'
        WHEN NEW.promedio_matematicas <= 4.5 THEN 'BAJO'
        ELSE 'BUENO'
    END;

    SET NEW.rendimiento_lenguaje = CASE
        WHEN NEW.promedio_lenguaje IS NULL THEN NULL
        WHEN NEW.promedio_lenguaje < 4.0 THEN 'EN RIESGO'
        WHEN NEW.promedio_lenguaje <= 4.5 THEN 'BAJO'
        ELSE 'BUENO'
    END;

    SET NEW.rendimiento_ingles = CASE
        WHEN NEW.promedio_ingles IS NULL THEN NULL
        WHEN NEW.promedio_ingles < 4.0 THEN 'EN RIESGO'
        WHEN NEW.promedio_ingles <= 4.5 THEN 'BAJO'
        ELSE 'BUENO'
    END;
END$$

CREATE TRIGGER notas_estudiante_bu
BEFORE UPDATE ON Notas_Estudiante
FOR EACH ROW
BEGIN
    SET NEW.rendimiento_matematicas = CASE
        WHEN NEW.promedio_matematicas IS NULL THEN NULL
        WHEN NEW.promedio_matematicas < 4.0 THEN 'EN RIESGO'
        WHEN NEW.promedio_matematicas <= 4.5 THEN 'BAJO'
        ELSE 'BUENO'
    END;

    SET NEW.rendimiento_lenguaje = CASE
        WHEN NEW.promedio_lenguaje IS NULL THEN NULL
        WHEN NEW.promedio_lenguaje < 4.0 THEN 'EN RIESGO'
        WHEN NEW.promedio_lenguaje <= 4.5 THEN 'BAJO'
        ELSE 'BUENO'
    END;

    SET NEW.rendimiento_ingles = CASE
        WHEN NEW.promedio_ingles IS NULL THEN NULL
        WHEN NEW.promedio_ingles < 4.0 THEN 'EN RIESGO'
        WHEN NEW.promedio_ingles <= 4.5 THEN 'BAJO'
        ELSE 'BUENO'
    END;
END$$

DELIMITER ;