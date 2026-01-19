-- Seed data para ramo_areaConocimiento (tabla puente)
-- Clasifica ramos por área de conocimiento

INSERT INTO Ramo_AreaConocimiento (id_ramo, id_area_conocimiento) VALUES
-- Ramos de Matemáticas (id_area = 1)
(1, 1), -- MAT101
(2, 1), -- MAT102
(3, 1), -- MAT201

-- Ramos de Inglés (id_area = 3)
(4, 3), -- IDEN01
(5, 3), -- IDEN02
(6, 3), -- IDEN03

-- Ramos de Lenguaje (id_area = 2)
(7, 2), -- LEN101
(8, 2), -- LEN102

-- Ramos técnicos (id_area = 5 - Tecnología)
(9, 5), -- TEC101

-- Ramos de salud (id_area = 4 - Ciencias)
(10, 4); -- SAL101
