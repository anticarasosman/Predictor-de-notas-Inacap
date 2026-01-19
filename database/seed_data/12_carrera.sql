-- Seed data para Carrera
-- Basado en programas de estudio del CSV

INSERT INTO Carrera (id_area_academica, id_institucion, id_plan_estudio, codigo_carrera, nombre_carrera, mencion, jornada, tipo_programa, activa) VALUES
-- Administración de Empresas (CFT)
(2, 1, 1, 'AE', 'Administración de Empresas', 'Sin Mención', 'VESPERTINA', 'REGULAR', TRUE),

-- Técnico en Odontología (CFT)
(1, 1, 2, 'OD', 'Técnico en Odontología', 'Sin Mención', 'DIURNA', 'REGULAR', TRUE),

-- Analista Programador (CFT)
(3, 1, 3, 'B5', 'Analista Programador', 'SIN MENCIÓN', 'VESPERTINA', 'REGULAR', TRUE);
