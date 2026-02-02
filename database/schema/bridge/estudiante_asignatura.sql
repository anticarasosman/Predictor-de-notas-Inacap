CREATE TABLE Estudiante_Asignatura (
    id_estudiante_asignatura INT PRIMARY KEY AUTO_INCREMENT,

    rut_estudiante VARCHAR(12),
    FOREIGN KEY (rut_estudiante) REFERENCES Estudiante(rut),

    codigo_asignatura VARCHAR(10),
    FOREIGN KEY (codigo_asignatura) REFERENCES Asignatura(codigo_asignatura),

    periodo_semestre VARCHAR(10),
    FOREIGN KEY (periodo_semestre) REFERENCES Semestre(periodo),

    nombre_docente VARCHAR(200),
    notas_parciales VARCHAR(100),
    
    porcentaje_asistencia INT,

    riesgo BOOLEAN DEFAULT FALSE,

    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
)