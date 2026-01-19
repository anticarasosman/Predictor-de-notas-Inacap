-- Seed data para Notas_Estudiante
-- Basado en datos CSV

INSERT INTO Notas_Estudiante (id_estudiante, promedio_matematicas, promedio_lenguaje, promedio_ingles, rendimiento_matematicas, rendimiento_lenguaje, rendimiento_ingles, semestre_ingreso) VALUES
-- Estudiantes con promedios
(1, 4.1, 4.7, 4.6, 'EN RIESGO', 'BAJO', 'BAJO', '2023-1'),
(4, 5.5, 6.0, 6.8, 'BAJO', 'BUENO', 'BUENO', '2023-1'),
(5, 6.5, 6.3, 6.8, 'BUENO', 'BUENO', 'BUENO', '2024-1'),
(7, 6.5, 6.3, 6.8, 'BUENO', 'BUENO', 'BUENO', '2025-1');
