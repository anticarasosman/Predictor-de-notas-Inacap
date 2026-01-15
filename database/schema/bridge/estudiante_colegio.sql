CREATE TABLE estudiante_colegio (
    id_estudiante INT NOT NULL,
    id_colegio INT NOT NULL,
    año_inicio INT NOT NULL,
    año_fin INT NOT NULL,
    
    PRIMARY KEY (id_estudiante, id_colegio),

    CONSTRAINT fk_ec_estudiante FOREIGN KEY (id_estudiante)
        REFERENCES Estudiante(id_estudiante) ON DELETE CASCADE,
    CONSTRAINT fk_ec_colegio FOREIGN KEY (id_colegio)
        REFERENCES Colegio(id_colegio) ON DELETE RESTRICT
)