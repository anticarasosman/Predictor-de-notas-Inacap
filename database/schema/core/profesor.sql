CREATE TABLE Profesor (
    id_profesor INT PRIMARY KEY AUTO_INCREMENT,

    nombre VARCHAR(100) NOT NULL,
    rut VARCHAR(12) NOT NULL UNIQUE,
    email_institucional VARCHAR(150) NOT NULL UNIQUE,
    telefono VARCHAR(15),
    fecha_nacimiento DATE,
    edad INT,
    sexo ENUM("MASCULINO", "FEMENINO", "OTRO"),

    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
)