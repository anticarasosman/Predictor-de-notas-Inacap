CREATE_TABLE Ramo (
    id_ramo INT PRIMARY KEY AUTO_INCREMENT,

    sigla VARCHAR(10) NOT NULL UNIQUE,
    nombre_ramo VARCHAR(200) NOT NULL,
    descripcion TEXT,
    horas_teoricas INT NOT NULL,
    horas_practicas INT NOT NULL,
    horas_semanales INT NOT NULL,
    /* En que semestre se recomienda tomar el ramo */
    nivel_recomendado INT NOT NULL,
    tiene_prerequisito BOOLEAN NOT NULL DEFAULT FALSE,
    activo BOOLEAN NOT NULL DEFAULT TRUE,

    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP

    UNIQUE (sigla, nombre_ramo)
)