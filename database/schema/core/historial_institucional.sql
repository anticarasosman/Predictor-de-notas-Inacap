CREATE TABLE HistorialInstitucional (
    id_historial_institucional INT PRIMARY KEY AUTO_INCREMENT,
    
    id_estudiante INT NOT NULL,
    FOREIGN KEY (id_estudiante)
        REFERENCES Estudiante(id_estudiante) ON DELETE CASCADE,

    institucion_anterior VARCHAR(200) NOT NULL,
    carrera_anterior VARCHAR(200) NOT NULL,
    ano_inicio INT NOT NULL,
    ano_finalizacion INT NOT NULL,
    motivo_retiro TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
)