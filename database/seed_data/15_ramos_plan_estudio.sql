-- Seed data para Ramos_Plan_Estudio
-- Relación entre planes de estudio y ramos

INSERT INTO Ramos_Plan_Estudio (semestre_plan, tipo_asignatura, orden_malla, activo_en_plan) VALUES
-- Primer semestre
(1, 'OBLIGATORIA', 1, TRUE),
(1, 'OBLIGATORIA', 2, TRUE),
(1, 'OBLIGATORIA', 3, TRUE),
-- Segundo semestre
(2, 'OBLIGATORIA', 4, TRUE),
(2, 'OBLIGATORIA', 5, TRUE),
-- Tercer semestre
(3, 'OBLIGATORIA', 6, TRUE);
