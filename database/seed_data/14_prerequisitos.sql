-- Seed data para Prerequisitos

INSERT INTO Prerequisitos (id_ramo, tipo_prerequisito) VALUES
-- MAT102 requiere MAT101
(2, 'OBLIGATORIO'),
-- MAT201 requiere MAT102
(3, 'OBLIGATORIO'),
-- IDEN02 requiere IDEN01
(5, 'OBLIGATORIO'),
-- IDEN03 requiere IDEN02
(6, 'OBLIGATORIO');
