-- Seed data para Ramo
-- Basado en categorías de programas de estudio

INSERT INTO Ramo (sigla, nombre_ramo, descripcion, horas_teoricas, horas_practicas, horas_semanales, nivel_recomendado, tiene_prerequisito, activo) VALUES
-- Ramos de Matemáticas
('MAT101', 'Matemática I', 'Fundamentos de matemática', 3, 2, 5, 1, FALSE, TRUE),
('MAT102', 'Matemática II', 'Álgebra y cálculo básico', 3, 2, 5, 2, TRUE, TRUE),
('MAT201', 'Cálculo I', 'Cálculo diferencial', 3, 2, 5, 3, TRUE, TRUE),

-- Ramos de Inglés
('IDEN01', 'Inglés I', 'Inglés básico', 2, 2, 4, 1, FALSE, TRUE),
('IDEN02', 'Inglés II', 'Inglés intermedio', 2, 2, 4, 2, TRUE, TRUE),
('IDEN03', 'Inglés III', 'Inglés avanzado', 2, 2, 4, 3, TRUE, TRUE),

-- Ramos de Lenguaje
('LEN101', 'Comunicación Efectiva', 'Técnicas de comunicación', 2, 2, 4, 1, FALSE, TRUE),
('LEN102', 'Taller de Escritura', 'Redacción y escritura académica', 2, 2, 4, 2, FALSE, TRUE),

-- Ramos técnicos
('TEC101', 'Introducción a la Programación', 'Fundamentos de programación', 2, 4, 6, 1, FALSE, TRUE),
('SAL101', 'Anatomía Básica', 'Fundamentos de anatomía', 3, 2, 5, 1, FALSE, TRUE);
