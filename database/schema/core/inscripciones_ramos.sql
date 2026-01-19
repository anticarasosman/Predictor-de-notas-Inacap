CREATE_TABLE Inscripciones_Ramos (
    id_inscripcion INT PRIMARY KEY AUTO_INCREMENT,

    id_estudiante INT NOT NULL,
    FOREIGN KEY (id_estudiante)
        REFERENCES Estudiante(id_estudiante) ON DELETE CASCADE,

    fecha_inscripcion DATE NOT NULL,
    tipo_inscripcion ENUM('REGULAR', 'CONVALIDACION', 'HOMOLOGACION') NOT NULL,
    estado_inscripcion ENUM('INSCRITO', 'RETIRADO', 'COMPLETADO') DEFAULT 'INSCRITO',
    nota_final DECIMAL(3,2) CHECK (nota_final BETWEEN 1.0 AND 7.0),
    porcentaje_asistencia DECIMAL(5,2) CHECK (porcentaje_asistencia BETWEEN 0.0 AND 100.0),
    situacion_final ENUM('APROBADO', 'REPROBADO', 'PENDIENTE') DEFAULT 'PENDIENTE',
    fecha_retiro DATE,
    motivo_retiro VARCHAR(255),

    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
)