-- Seed data para Direccion
-- Depende de Comuna

INSERT INTO Direccion (id_comuna, calle, numero, tipo_direccion) VALUES
-- Direcciones en Coyhaique (id_comuna = 1)
(1, 'Cipreses', 509, 'Permanente'),
(1, 'Calle Principal', 123, 'Permanente'),
(1, 'Avenida Baquedano', 456, 'Temporal'),
-- Direcciones en Santiago (id_comuna = 3)
(3, 'Alameda', 1000, 'Permanente'),
(3, 'Apoquindo', 2000, 'Permanente');
