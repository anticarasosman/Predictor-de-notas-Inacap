INSERT INTO Asignatura (
	codigo_asignatura,
	nombre,
	programa,
	area,
	COD_mencion,
	mencion,
	plan,
	modalidad,
	nivel,
	prerequisito_semestre_siguiente,
	ultimo_nivel
) VALUES
(
	'INF101', 'Fundamentos de Programación', 'Ingeniería en Informática', 'Programación',
	'INF', 'General', '2023', 'DIURNA', 1, 0, 8
),
(
	'MAT120', 'Matemática I', 'Ingeniería en Informática', 'Matemática',
	'INF', 'General', '2023', 'DIURNA', 1, 0, 8
),
(
	'ADM210', 'Gestión Empresarial', 'Administración de Empresas', 'Gestión',
	'ADM', 'Gestión', '2022', 'VESPERTINA', 3, 2, 6
),
(
	'SOC130', 'Intervención Social I', 'Trabajo Social', 'Social',
	'TS', 'Comunitaria', '2021', 'DIURNA', 2, 1, 8
),
(
	'PROG200', 'Programación Orientada a Objetos', 'Analista Programador', 'Programación',
	'AP', 'Desarrollo', '2022', 'VESPERTINA', 2, 1, 4
);
