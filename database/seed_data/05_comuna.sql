-- Seed data para Comuna
-- Depende de Region

INSERT INTO Comuna (id_region, codigo, nombre) VALUES
-- Región de Aysén (id_region = 1)
(1, 11101, 'Coyhaique'),
(1, 11102, 'Puerto Aysén'),
-- Región Metropolitana (id_region = 2)
(2, 13101, 'Santiago'),
(2, 13102, 'Providencia'),
-- Valparaíso (id_region = 3)
(3, 5101, 'Valparaíso'),
(3, 5102, 'Viña del Mar');
