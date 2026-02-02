INSERT INTO Asignatura_semestre (
	codigo_asignatura,
	periodo_semestre,
	secciones,
	alumnos,
	porcentaje_reprobacion_N1,
	porcentaje_reprobacion_N2,
	porcentaje_reprobacion_N3,
	alumnos_en_riesgo,
	alumnos_ayudantia,
	promedio_nota_uno,
	promedio_nota_dos,
	promedio_nota_tres,
	ayudantia_virtual,
	ayudantia_sede
) VALUES
('INF101', '2026-primavera', 3, 90, 12, 8, 5, 14, 20, 5.4, 5.6, 5.8, TRUE, TRUE),
('MAT120', '2026-primavera', 2, 70, 15, 10, 7, 18, 22, 5.0, 5.3, 5.5, TRUE, FALSE),
('ADM210', '2025-otoño', 1, 35, 8, 6, 4, 6, 5, 5.2, 5.4, 5.6, FALSE, TRUE),
('SOC130', '2025-otoño', 2, 60, 5, 4, 3, 7, 10, 5.8, 5.9, 6.0, FALSE, FALSE),
('PROG200', '2026-primavera', 2, 50, 10, 7, 6, 9, 12, 5.5, 5.7, 5.9, TRUE, TRUE),
('INF101', '2026-otoño', 2, 65, 11, 9, 6, 12, 15, 5.3, 5.5, 5.7, TRUE, FALSE);
