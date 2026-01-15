CREATE TABLE Comuna (
    PRIMARY KEY id_comuna INT AUTO_INCREMENT,

    id_region INT NOT NULL,
    FOREIGN KEY (id_region)
        REFERENCES Region(id_region) ON DELETE RESTRICT,

    codigo INT UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    
    UNIQUE (nombre, id_region)

)