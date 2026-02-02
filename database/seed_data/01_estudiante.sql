INSERT INTO Estudiante (
	rut,
	secciones_curriculares,
	secciones_online,
	deuda,
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
	'12.345.678-9', 5, 2, 0, 92, 'Camila Rojas', 'Ingeniería en Informática', 'Luis Rojas',
	FALSE, TRUE, FALSE, FALSE, FALSE, TRUE, 'NUEVO', 'MATRICULADO', 6.2, 6.0, 5.8, '2026-01-28'
),
(
	'9.876.543-2', 4, 1, 120000, 85, 'Diego Pérez', 'Administración de Empresas', 'Marta Pérez',
	FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, 'VIEJO', 'ACTIVO', 5.4, 5.8, 5.1, '2026-01-30'
),
(
	'18.234.567-1', 6, 0, 450000, 70, 'Valentina Soto', 'Trabajo Social', 'Carolina Soto',
	FALSE, TRUE, TRUE, TRUE, FALSE, FALSE, 'VIEJO', 'PENDIENTE', 5.9, 6.1, 5.6, '2025-12-15'
),
(
	'7.654.321-0', 3, 3, 0, 96, 'Javier Morales', 'Analista Programador', 'Ana Morales',
	TRUE, FALSE, FALSE, FALSE, FALSE, TRUE, 'VIEJO', 'MATRICULADO', 6.5, 6.3, 6.0, '2026-01-27'
),
(
	'21.345.987-6', 5, 1, 80000, 78, 'Fernanda López', 'Contabilidad', 'Rosa López',
	FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, 'NUEVO', 'EN POSTULACION', 5.7, 5.5, 5.2, '2026-01-25'
);
