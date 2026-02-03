INSERT INTO Estudiante (
	rut,
	secciones_curriculares,
	secciones_online,
	asistencia_promedio,
	nombre,
	programa_estudio,
	nombre_apoderado,
	terminal,
	tiene_gratuidad,
	solicitud_interrupcion_estudios,
	solicitud_interrupcion_estudio_pendiente,
	interrupcion_estudio_pendiente,
	beca_stem,
	tipo_alumno,
	estado_matricula,
	promedio_media_matematica,
	promedio_media_lenguaje,
	promedio_media_ingles,
	ultima_asistencia
) VALUES
(
	'12345678-9', 5, 2, 0, 'Camila Rojas', 'Ingeniería en Informática', 'Luis Rojas',
	FALSE, TRUE, FALSE, FALSE, FALSE, TRUE, 'NUEVO', 'MATRICULADO', 6.2, 6.0, 5.8, '2026-01-28'
),
(
	'9876543-2', 4, 1, 85, 'Diego Pérez', 'Administración de Empresas', 'Marta Pérez',
	FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, 'VIEJO', 'ACTIVO', 5.4, 5.8, 5.1, '2026-01-30'
),
(
	'18234567-1', 6, 0, 70, 'Valentina Soto', 'Trabajo Social', 'Carolina Soto',
	FALSE, TRUE, TRUE, TRUE, FALSE, FALSE, 'VIEJO', 'PENDIENTE', 5.9, 6.1, 5.6, '2025-12-15'
),
(
	'7654321-0', 3, 3, 0, 'Javier Morales', 'Analista Programador', 'Ana Morales',
	TRUE, FALSE, FALSE, FALSE, FALSE, TRUE, 'VIEJO', 'MATRICULADO', 6.5, 6.3, 6.0, '2026-01-27'
),
(
	'21345987-6', 5, 1, 80000, 'Fernanda López', 'Contabilidad', 'Rosa López',
	FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, 'NUEVO', 'EN POSTULACION', 5.7, 5.5, 5.2, '2026-01-25'
);
