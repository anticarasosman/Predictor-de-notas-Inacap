CREATE_TABLE Secciones_Ramos(
    id_seccion_ramo INT PRIMARY KEY AUTO_INCREMENT,

    id_ramo INT NOT NULL,
    FOREIGN KEY (id_ramo) REFERENCES Ramo(id_ramo) ON DELETE CASCADE

    seccion VARCHAR(10) NOT NULL,
    horario VARCHAR(100) NOT NULL,
    /* Aun no se si quieren implementar perfiles de profesores en la base de datos */
    /*profesor VARCHAR(100) NOT NULL,*/
    codigo_seccion VARCHAR(50) UNIQUE NOT NULL,
    /* El formato es 20XX-X (Ej: 2do semestre de 2025 seria 2025-2) */
    semestre_dictado VARCHAR(10) NOT NULL,
    cupos_totales INT NOT NULL,
    cupos_ocupados INT NOT NULL,
    cupos_disponibles INT NOT NULL GENERATED ALWAYS AS (cupos_totales - cupos_ocupados) STORED,
    horario TEXT NOT NULL,
    estado ENUM("ACTIVA", "CANCELADA", "LLENA") NOT NULL,

    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    UNIQUE (id_ramo_plan_estudio, seccion)
)