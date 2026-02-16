-- Este archivo agrega los estudiantes existentes en la BD a semestres
-- para demostración de la funcionalidad de exportación

INSERT INTO Estudiante_Semestre (
	rut_estudiante,
	periodo_semestre,
	asignaturas_PE,
	asignaturas_reprobadas_cuatro_veces,
	asignaturas_reprobadas_tres_veces,
	solicitud_reingreso
) VALUES
-- FABIOLA JEANETTE LAVADO MANSILLA (10288158-3)
('10288158-3', '2025-otoño', 6, 0, 1, FALSE),
('10288158-3', '2026-primavera', 5, 0, 0, FALSE),

-- ANA MARÍA CHRISTENSEN ARTEAGA (10340398-7)
('10340398-7', '2025-otoño', 6, 0, 1, FALSE),
('10340398-7', '2026-primavera', 6, 0, 0, FALSE),
('10340398-7', '2026-otoño', 5, 0, 0, FALSE),

-- LEONTINA ESTER JARA ARIAS (10548222-1)
('10548222-1', '2025-otoño', 5, 1, 0, FALSE),
('10548222-1', '2026-primavera', 6, 0, 1, FALSE),

-- CLAUDIA XIMENA ROJAS SAN MARTÍN (10941044-6)
('10941044-6', '2025-otoño', 6, 0, 1, FALSE),
('10941044-6', '2026-primavera', 5, 0, 0, FALSE),
('10941044-6', '2026-otoño', 6, 0, 0, FALSE),

-- SELMA RAMONA ALVARADO SEGOVIA (11415014-2)
('11415014-2', '2025-otoño', 6, 0, 1, FALSE),
('11415014-2', '2026-primavera', 6, 0, 0, FALSE),

-- SANDRA ARACELY TOLEDO VARGAS (11910674-5)
('11910674-5', '2025-otoño', 5, 0, 0, FALSE),
('11910674-5', '2026-primavera', 5, 0, 1, FALSE),
('11910674-5', '2026-otoño', 4, 0, 0, FALSE),

-- ESTER DEL CARMEN GONZÁLEZ VARGAS (12310754-3)
('12310754-3', '2025-otoño', 6, 0, 0, FALSE),
('12310754-3', '2026-primavera', 6, 0, 0, FALSE),
('12310754-3', '2026-otoño', 5, 0, 0, FALSE),

-- MARÍA ANGÉLICA DÍAZ GONZÁLEZ (12503757-7)
('12503757-7', '2025-otoño', 6, 0, 1, FALSE),
('12503757-7', '2026-primavera', 6, 0, 0, FALSE),

-- CRISTIAN ALEJANDRO PROVOSTE VIDAL (12936098-4)
('12936098-4', '2025-otoño', 6, 0, 1, FALSE),
('12936098-4', '2026-primavera', 5, 0, 0, FALSE),
('12936098-4', '2026-otoño', 6, 0, 0, FALSE),

-- LORENA PAULINA DOMÍNGUEZ CRUZ (12971655-K)
('12971655-K', '2025-otoño', 6, 0, 0, FALSE),
('12971655-K', '2026-primavera', 6, 0, 0, FALSE),
('12971655-K', '2026-otoño', 5, 0, 0, FALSE),

-- ALEJANDRA CECILIA DI GIOVANNI REYNAGA (13288004-2)
('13288004-2', '2025-otoño', 6, 0, 1, FALSE),
('13288004-2', '2026-primavera', 6, 0, 0, FALSE),

-- ALEX NELSON MORA MERA (13728795-1)
('13728795-1', '2025-otoño', 6, 0, 1, FALSE),
('13728795-1', '2026-primavera', 5, 0, 0, FALSE),
('13728795-1', '2026-otoño', 6, 0, 0, FALSE),

-- ROBERTO MAURICIO CURIÑANCO RIVERA (13742774-5)
('13742774-5', '2025-otoño', 6, 0, 1, FALSE),
('13742774-5', '2026-primavera', 6, 0, 0, FALSE),

-- VIVIANA MELIZA HERNÁNDEZ HERNÁNDEZ (13758202-3)
('13758202-3', '2025-otoño', 5, 0, 0, FALSE),
('13758202-3', '2026-primavera', 5, 0, 0, FALSE),
('13758202-3', '2026-otoño', 4, 0, 1, FALSE),

-- ALEJANDRA CAROLINA ÁLVAREZ MELLADO (13826412-2)
('13826412-2', '2025-otoño', 6, 0, 0, FALSE),
('13826412-2', '2026-primavera', 6, 0, 0, FALSE),

-- ELIZABETH DEL CARMEN NAVARRETE MALDONADO (13969991-2)
('13969991-2', '2025-otoño', 6, 0, 1, FALSE),
('13969991-2', '2026-primavera', 5, 0, 0, FALSE),
('13969991-2', '2026-otoño', 6, 0, 0, FALSE),

-- FABIOLA DEL CARMEN LEPIO MONTIEL (13970029-5)
('13970029-5', '2025-otoño', 6, 0, 1, FALSE),
('13970029-5', '2026-primavera', 6, 0, 0, FALSE),
('13970029-5', '2026-otoño', 5, 0, 0, FALSE),

-- TAMARA BEATRIZ HERNÁNDEZ ARIAS (14043063-3)
('14043063-3', '2025-otoño', 6, 0, 1, FALSE),
('14043063-3', '2026-primavera', 6, 0, 0, FALSE),
('14043063-3', '2026-otoño', 5, 0, 0, FALSE);
