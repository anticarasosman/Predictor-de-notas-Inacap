CREATE_TABLE Institucion(
    id_institucion INT PRIMARY KEY AUTO_INCREMENT,
    tipo_instucion ENUM("C.F.T", "I:P"),
    nombre_institucion VARCHAR(200) NOT NULL UNIQUE,
    
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    UNIQUE (tipo_instucion, nombre_institucion)
)