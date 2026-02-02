CREATE TABLE Estudiante_Semestre (
    id_estudiante_semestre INT PRIMARY KEY AUTO_INCREMENT,

    rut_estudiante VARCHAR(12),
    FOREIGN KEY (rut_estudiante) REFERENCES Estudiante(rut),
    periodo_semestre VARCHAR(20),
    FOREIGN KEY (periodo_semestre) REFERENCES Semestre(periodo),

    asignaturas_PE INT,
    asignaturas_reprobadas_cuatro_veces INT,
    asignaturas_reprobadas_tres_veces INT,
    
    solicitud_reingreso BOOLEAN DEFAULT FALSE,

    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
)