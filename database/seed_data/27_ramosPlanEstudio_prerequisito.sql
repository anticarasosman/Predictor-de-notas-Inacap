-- Seed data para Ramos_Plan_Estudio_Prerequisito (tabla puente)
-- Relaciona ramos del plan con sus prerequisitos

INSERT INTO Ramos_Plan_Estudio_Prequsito (id_ramo_plan_estudio, id_prerequisito) VALUES
-- MAT102 (ramo_plan 2) requiere prerequisito 1
(2, 1),

-- MAT201 (ramo_plan 3) requiere prerequisito 2
(3, 2),

-- IDEN02 (ramo_plan 5) requiere prerequisito 3
(5, 3),

-- IDEN03 (ramo_plan 6) requiere prerequisito 4
(6, 4);
