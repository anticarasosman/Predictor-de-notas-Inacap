CREATE TABLE Comuna (
    id_comuna INT PRIMARY KEY AUTO_INCREMENT,

    FOREIGN KEY (id_region)
        REFERENCES Region(id_region) ON DELETE RESTRICT,

    id_region INT NOT NULL,
    codigo INT UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    UNIQUE (nombre, id_region)
)