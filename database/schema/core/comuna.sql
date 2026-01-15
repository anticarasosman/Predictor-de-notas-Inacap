CREATE TABLE Comuna (
    id_comuna INT PRIMARY KEY AUTO_INCREMENT,

    id_region INT NOT NULL,
    codigo INT UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    
    FOREIGN KEY (id_region)
        REFERENCES Region(id_region) ON DELETE RESTRICT,
    
    UNIQUE (nombre, id_region)
)