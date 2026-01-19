CREATE_TABLE Notas_Estudiante (
    id_nota INT PRIMARY KEY AUTO_INCREMENT,

    id_estudiante INT NOT NULL,
    FOREIGN KEY (id_estudiante)
        REFERENCES Estudiante(id_estudiante) ON DELETE CASCADE,
    
    promedio_matematicas DECIMAL(3,2) CHECK (promedio_matematicas BETWEEN 1.0 AND 7.0),
    promedio_lenguaje DECIMAL(3,2) CHECK (promedio_lenguaje BETWEEN 1.0 AND 7.0),
    promedio_ingles DECIMAL(3,2) CHECK (promedio_ingles BETWEEN 1.0 AND 7.0),
    rendimiento_matematicas ENUM("EN RIESGO", "BAJO", "BUENO")
    rendimiento_lenguaje ENUM("EN RIESGO", "BAJO", "BUENO"),
    rendimiento_ingles ENUM("EN RIESGO", "BAJO", "BUENO"),
    /* El formato para los semestres es 20XX-(1 o 2)*/
    semestre_ingreso VARCHAR(10) NOT NULL,

    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP

    UNIQUE (id_estudiante, año_registro, semestre_registro)
)