INSERT INTO Estudiante_Semestre (
	rut_estudiante,
	periodo_semestre,
	asignaturas_PE,
	asignaturas_reprobadas_cuatro_veces,
	asignaturas_reprobadas_tres_veces,
	solicitud_reingreso
) VALUES
('12345678-9', '2026-primavera', 5, 0, 0, FALSE),
('9876543-2', '2025-otoño', 4, 0, 1, FALSE),
('18234567-1', '2025-otoño', 6, 0, 2, TRUE),
('7654321-0', '2026-primavera', 3, 0, 0, FALSE),
('21345987-6', '2026-primavera', 5, 0, 0, FALSE),
('9876543-2', '2026-primavera', 3, 0, 0, FALSE);
