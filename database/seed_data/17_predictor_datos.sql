-- Seed data para Predictor_Datos
-- Datos del predictor de progresión

INSERT INTO Predictor_Datos (id_estudiante, id_matricula, rinde_matematicas, logro_porcentaje, requiere_rendir, ano_evaluacion, semestre_evaluacion, fecha_evaluacion, objetivo, metodos, proceso) VALUES
(1, 1, TRUE, 50, TRUE, 2025, '2025-1', '2025-03-15', 'Mejorar rendimiento en matemáticas', 'Clases de refuerzo, talleres', 'En proceso'),
(2, 2, TRUE, 30, FALSE, 2025, '2025-1', '2025-03-15', 'Mantener rendimiento', 'Estudio regular', 'Completado'),
(4, 4, TRUE, 73, FALSE, 2025, '2025-1', '2025-03-15', 'Aprobar con buen nivel', 'Estudio autónomo', 'En proceso');
