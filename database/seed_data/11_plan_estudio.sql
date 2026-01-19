-- Seed data para Plan_Estudio
-- Nota: Esta tabla tiene dependencia con Ramo, ajustar schema si es necesario

INSERT INTO Plan_Estudio (id_ramo, codigo_plan_estudio, nombre_plan_estudio, ano_vigencia, semestre_vigencia, estado, duracion_estimada_semestres, descripcion, fecha_inicio) VALUES
(1, 'PLAN-AE-2024', 'Plan Administración de Empresas 2024', 2024, 1, 'VIGENTE', 4, 'Plan de estudios vigente para Administración de Empresas', '2024-03-01'),
(2, 'PLAN-OD-2024', 'Plan Técnico en Odontología 2024', 2024, 1, 'VIGENTE', 4, 'Plan de estudios vigente para Técnico en Odontología', '2024-03-01'),
(3, 'PLAN-AP-2024', 'Plan Analista Programador 2024', 2024, 1, 'VIGENTE', 5, 'Plan de estudios vigente para Analista Programador', '2024-03-01');