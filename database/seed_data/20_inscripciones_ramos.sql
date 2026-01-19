-- Seed data para Inscripciones_Ramos
-- Inscripciones de estudiantes a secciones

INSERT INTO Inscripciones_Ramos (id_estudiante, id_seccion, fecha_inscripcion, tipo_inscripcion, estado_inscripcion, nota_final, porcentaje_asistencia, situacion_final) VALUES
-- Anahí Formantel en Inglés II
(4, 1, '2025-03-10', 'REGULAR', 'COMPLETADO', 6.60, 90.00, 'APROBADO'),

-- Javiera Mansilla en Inglés II
(5, 1, '2025-03-10', 'REGULAR', 'COMPLETADO', 6.90, 82.00, 'APROBADO'),

-- Natalia Ojeda en Inglés II
(6, 1, '2025-03-10', 'REGULAR', 'COMPLETADO', 6.60, 90.00, 'APROBADO');
