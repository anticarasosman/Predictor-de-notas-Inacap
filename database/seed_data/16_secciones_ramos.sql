-- Seed data para Secciones_Ramos
-- Secciones disponibles para inscripción

INSERT INTO Secciones_Ramos (id_ramo, id_profesor, seccion, horario, codigo_seccion, semestre_dictado, jornadas, cupos_totales, cupos_ocupados, estado) VALUES
-- Inglés II (IDEN02) - Sección OD
(5, 4, 'OD-2-N4-C1', 'Lunes y Miércoles 14:00-16:00', 'IDEN02-OD-2025-1', '2025-1', 'DIURNA', 30, 3, 'ACTIVA'),

-- Matemática I
(1, 1, 'MAT-1-A', 'Martes y Jueves 08:00-10:00', 'MAT101-A-2025-1', '2025-1', 'DIURNA', 35, 10, 'ACTIVA'),

-- Comunicación Efectiva
(7, 7, 'COM-1-V', 'Lunes y Miércoles 18:00-20:00', 'LEN101-V-2025-1', '2025-1', 'VESPERTINA', 30, 8, 'ACTIVA');
