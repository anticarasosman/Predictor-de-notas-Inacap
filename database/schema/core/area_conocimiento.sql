CREATE_TABLE Area_Conocimiento(
    id_area_conocimiento INT PRIMARY KEY AUTO_INCREMENT,

    nombre_area_conocimiento VARCHAR(200) NOT NULL UNIQUE,
    descripcion TEXT,
    color VARCHAR(7) NOT NULL UNIQUE
)