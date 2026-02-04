CREATE TABLE Reporte_financiero_estudiante (
    id INT PRIMARY KEY AUTO_INCREMENT,

    rut_estudiante VARCHAR(12),
    FOREIGN KEY (rut_estudiante) REFERENCES Estudiante(rut),

    cantidad_cuotas_pendientes_matriculas INT,
    cantidad_cuotas_pendientes_colegiaturas INT,
    deuda_matriculas INT,
    deuda_colegiaturas INT,
    otras_deudas INT,
    deuda_total INT,

    fecha_generacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;