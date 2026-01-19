CREATE_TABLE Planes_Estudio (
    id_plan_estudio INT PRIMARY KEY AUTO_INCREMENT,

    id_ramo INT NOT NULL,
    FOREIGN KEY (id_ramo) REFERENCES Ramo(id_ramo) ON DELETE CASCADE RESTRICT,

    codigo_plan_estudio VARCHAR(20) NOT NULL UNIQUE,
    nombre_plan_estudio VARCHAR(200) NOT NULL UNIQUE,
    año_vigencia INT NOT NULL,
    semestre_vigencia INT NOT NULL,
    estado ENUM("VIGENTE", "INACTIVO") NOT NULL,
    total_creditos INT NOT NULL,
    descripcion TEXT,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE,

    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
)