CREATE TABLE Matricula(
    id_matricula INT PRIMARY KEY AUTO_INCREMENT,

    id_estudiante INT NOT NULL,
    FOREIGN KEY (id_estudiante)
        REFERENCES Estudiante(id_estudiante) ON DELETE CASCADE,
    id_carrera INT NOT NULL,
    FOREIGN KEY (id_carrera)
        REFERENCES Carrera(id_carrera) ON DELETE CASCADE,
    id_predictor_datos INT NOT NULL,
    FOREIGN KEY (id_predictor_datos)
        REFERENCES Predictor_Datos(id_predictor_datos) ON DELETE CASCADE,

    /* El formato para los semestres es 20XX-(1 o 2)*/
    semestre_ingreso VARCHAR(10) NOT NULL,
    ultimo_semestre_cursado VARCHAR(10) NOT NULL,
    tipo_estudiante ENUM('NUEVO', 'ANTIGUO', 'TRANSFERIDO') NOT NULL,
    es_candidato_a_gratuacion BOOLEAN DEFAULT FALSE,
    es_trabajador BOOLEAN DEFAULT FALSE,
    es_reincorporado BOOLEAN DEFAULT FALSE,
    estado_matricula ENUM('ACTIVA', 'PENDIENTE', 'EN POSTULACION', "MATRICULADO", "LISTA DE ESPERA", "CANCELADO") DEFAULT 'ACTIVA',
    /* Nivel academico del estudiantes */
    nivel_actual ENUM('PREESCOLAR', "PRIMARIO", 'SECUNDARIO', "BACHILLERATO", "LICENCIATURA", "MAESTRIA", "DOCTORADO") NOT NULL,
    numero_de_convalidaciones INT DEFAULT 0,
    numero de homologaciones INT DEFAULT 0,
    cantidad_examenes_competencia INT DEFAULT 0,
    cantidad_asignaturas_actuales INT DEFAULT 0,
    fecha_matricula DATE NOT NULL,
    cambio_sede VARCHAR(100),
    programa_anterior VARCHAR(100),
    
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP

    UNIQUE (id_estudiante, semestre_ingreso, id_carrera)
)