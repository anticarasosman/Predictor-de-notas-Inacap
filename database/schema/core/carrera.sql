CREATE TABLE Carrera (
    id_carrera INT PRIMARY KEY AUTO_INCREMENT,

    id_area_academica INT NOT NULL,
    FOREIGN KEY (id_area_academica)
        REFERENCES Area_Academica(id_area_academica) ON DELETE CASCADE,
    id_institucion INT NOT NULL,
    FOREIGN KEY (id_institucion)
        REFERENCES Institucion(id_institucion) ON DELETE CASCADE,
    id_plan_estudio INT NOT NULL,
    FOREIGN KEY (id_plan_estudio)
        REFERENCES Plan_Estudio(id_plan_estudio) ON DELETE CASCADE,
    
    codigo_carrera VARCHAR(20) NOT NULL UNIQUE,
    nombre_carrera VARCHAR(200), NOT NULL, UNIQUE,
    mencion VARCHAR(100),
    jornada ENUM("DIURNA", "VESPERTINA", "MIXTA") NOT NULL,
    tipo_programa ENUM("REGULAR", "PEEC"),
    activa BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
)