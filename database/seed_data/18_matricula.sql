-- Seed data para Matricula
-- Matrículas activas de estudiantes

INSERT INTO Matricula (id_estudiante, id_carrera, semestre_ingreso, ultimo_semestre_cursado, tipo_estudiante, es_candidato_a_gratuacion, es_trabajador, es_reincorporado, estado_matricula, nivel_actual, numero_de_convalidaciones, numero_de_homologaciones, cantidad_examenes_competencia, cantidad_asignaturas_actuales, fecha_matricula) VALUES
-- Camila Manríquez - Administración de Empresas
(1, 1, '2023-1', '2024-2', 'ANTIGUO', FALSE, FALSE, FALSE, 'ACTIVA', 'LICENCIATURA', 0, 0, 0, 6, '2023-03-15'),

-- Tammy Adriazola - Administración de Empresas
(2, 1, '2023-1', '2024-2', 'ANTIGUO', FALSE, FALSE, FALSE, 'ACTIVA', 'LICENCIATURA', 0, 0, 0, 6, '2023-03-15'),

-- María Valencia - Administración de Empresas
(3, 1, '2024-1', '2024-2', 'ANTIGUO', FALSE, FALSE, FALSE, 'ACTIVA', 'LICENCIATURA', 0, 0, 0, 5, '2024-03-15'),

-- Anahí Formantel - Técnico en Odontología
(4, 2, '2023-1', '2024-2', 'ANTIGUO', FALSE, FALSE, FALSE, 'ACTIVA', 'LICENCIATURA', 0, 0, 0, 6, '2023-03-15'),

-- Javiera Mansilla - Técnico en Odontología
(5, 2, '2024-1', '2024-2', 'ANTIGUO', FALSE, FALSE, FALSE, 'ACTIVA', 'LICENCIATURA', 0, 0, 0, 6, '2024-03-15'),

-- Natalia Ojeda - Técnico en Odontología
(6, 2, '2024-1', '2024-2', 'ANTIGUO', FALSE, FALSE, FALSE, 'ACTIVA', 'LICENCIATURA', 0, 0, 0, 6, '2024-03-15'),

-- Dante Agüero - Analista Programador
(7, 3, '2025-1', '2025-1', 'NUEVO', FALSE, FALSE, FALSE, 'ACTIVA', 'LICENCIATURA', 0, 0, 0, 6, '2025-03-01'),

-- Andrea Belmar - Administración de Empresas
(8, 1, '2025-1', '2025-1', 'NUEVO', FALSE, TRUE, FALSE, 'ACTIVA', 'LICENCIATURA', 0, 0, 0, 6, '2025-03-01');