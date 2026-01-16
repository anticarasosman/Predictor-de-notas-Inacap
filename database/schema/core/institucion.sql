CREATE_TABLE Institucion(
    id_institucion INT PRIMARY KEY AUTO_INCREMENT,
    tipo_instucion ENUM("C.F.T", "I:P"),
    nombre_institucion VARCHAR(200) NOT NULL UNIQUE,
    UNIQUE (tipo_instucion, nombre_institucion)
)