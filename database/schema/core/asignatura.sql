CREATE TABLE Asignatura(
    codigo_asignatura VARCHAR(10) PRIMARY KEY,

    nombre VARCHAR(200),
    programa VARCHAR(100),
    area VARCHAR(100),
    COD_mencion VARCHAR(10),
    mencion VARCHAR(100),
    plan VARCHAR(30),

    modalidad ENUM("VESPERTINA", "DIURNA"),
    
    nivel INT,
    prerequisito_semestre_siguiente INT,
    ultimo_nivel INT,

    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;