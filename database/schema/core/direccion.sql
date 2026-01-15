CREATE TABLE Direccion (
    id_direccion INT PRIMARY KEY AUTO_INCREMENT,

    id_comuna INT NOT NULL,
    FOREIGN KEY (id_comuna)
        REFERENCES Comuna(id_comuna) ON DELETE RESTRICT,

    calle VARCHAR(200) NOT NULL,
    numero INT NOT NULL,
    departamento VARCHAR(50),
    poblacion_villa VARCHAR(100),
    tipo_direccion ENUM("Permanente", "Temporal") NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)