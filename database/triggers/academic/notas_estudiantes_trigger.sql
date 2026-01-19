DROP TRIGGER IF EXISTS notas_estudiante_before_insert;
DELIMITER //
CREATE TRIGGER ramos_plan_estudio_before_insert
BEFORE INSERT ON Notas_Estudiante
FOR EACH ROW
BEGIN
    IF NEW.promedio_matematicas > 0 AND NEW.promedio_matematicas < 4.0 THEN
        SET NEW.rendimiento_matematicas = "EN RIESGO";
END;