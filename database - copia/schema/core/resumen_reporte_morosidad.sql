CREATE TABLE Resumen_reporte_morosidad (
    id INT PRIMARY KEY AUTO_INCREMENT,

    -- Información de fecha
    fecha_actualizacion DATE NOT NULL,
    
    -- Totales de estudiantes
    numero_estudiantes_total INT NOT NULL,
    
    -- Deudores
    numero_estudiantes_con_deuda INT NOT NULL,
    porcentaje_estudiantes_con_deuda DECIMAL(5, 2),
    
    -- Montos de deuda
    monto_total_adeudado INT NOT NULL DEFAULT 0,
    monto_total_compromisos INT NOT NULL DEFAULT 0,
    
    -- Promedio de cuotas
    promedio_cuotas_pendientes DECIMAL(8, 2),
    
    -- Porcentaje de morosidad
    porcentaje_morosidad DECIMAL(5, 2),

    -- Timestamp de creación del registro
    fecha_generacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE KEY unique_fecha_actualizacion (fecha_actualizacion)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
