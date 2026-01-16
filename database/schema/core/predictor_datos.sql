CREATE TABLE PredictorDatos (
    id_predictor_datos INT PRIMARY KEY AUTO_INCREMENT,
    
    id_estudiante INT NOT NULL,
    id_matricula INT NOT NULL,
    rinde_matematicas BOOLEAN,
    logro_porcentaje INT,
    requiere_rendir BOOLEAN,
    año_evaluacion INT,
    semestre_evaluacion VARCHAR(10), /* El formato de semestre_evalucion es 20##-1 (Ej: Primer semestre de 2025 es 2025-1) */
    fecha_evaluacion DATE,
    objetivo TEXT,
    metodos TEXT,
    proceso TEXT,
    observaciones TEXT,

    UNIQUE (id_estudiante, año_evaluacion, semestre_evaluacion),

    FOREIGN KEY (id_estudiante)
        REFERENCES Estudiante(id_estudiante) ON DELETE CASCADE,
    FOREIGN KEY (id_matricula)
        REFERENCES Matricula(id_matricula) ON DELETE CASCADE
)