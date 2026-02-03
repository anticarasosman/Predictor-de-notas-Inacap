CREATE TABLE Asignatura_semestre (
    id_asignatura_semestre INT PRIMARY KEY AUTO_INCREMENT,

    codigo_asignatura VARCHAR(10),
    FOREIGN KEY (codigo_asignatura) REFERENCES Asignatura(codigo_asignatura),

    periodo_semestre VARCHAR(20),
    FOREIGN KEY (periodo_semestre) REFERENCES Semestre(periodo),

    secciones INT,
    alumnos INT,
    alumnos_en_riesgo INT,
    alumnos_ayudantia INT,
    
    porcentaje_reprobacion_N1 FLOAT,
    porcentaje_reprobacion_N2 FLOAT,
    porcentaje_reprobacion_N3 FLOAT,
    
    promedio_nota_uno DECIMAL(2,1),
    promedio_nota_dos DECIMAL(2,1),
    promedio_nota_tres DECIMAL(2,1),
    
    ayudantia_virtual BOOLEAN DEFAULT FALSE,
    ayudantia_sede BOOLEAN DEFAULT FALSE,

    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;