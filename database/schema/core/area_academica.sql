CREATE_TABLE Area_Academica(
    id_area_academica INT PRIMARY KEY AUTO_INCREMENT,

    nombre_area_academica VARCHAR(200) NOT NULL UNIQUE,
    descripcion TEXT,

    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
)