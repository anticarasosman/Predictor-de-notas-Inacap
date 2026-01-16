CREATE TABLE Estudiante (
    id_estudiante INT PRIMARY KEY AUTO_INCREMENT,

    rut VARCHAR(12) NOT NULL UNIQUE,
    nombre VARCHAR(200) NOT NULL,
    email_institucional VARCHAR(200) NOT NULL UNIQUE,
    telefono VARCHAR(20) NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    edad INT NOT NULL,
    sexo ENUM('M', 'F', 'O') NOT NULL,
    nacionalidad VARCHAR(100) NOT NULL,
    ano_egreso_media INT NOT NULL,
    puntaje_psu INT NOT NULL,
    integrantes_grupo_familiar INT NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    email_personal VARCHAR(200) UNIQUE
)