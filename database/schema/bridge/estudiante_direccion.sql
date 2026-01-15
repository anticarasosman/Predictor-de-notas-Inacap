CREATE TABLE estudiante_direccion (
    id_estudiante INT NOT NULL,
    id_direccion INT NOT NULL,
    PRIMARY KEY (id_estudiante, id_direccion),

    CONSTRAINT fk_ed_estudiante FOREIGN KEY (id_estudiante)
        REFERENCES Estudiante(id_estudiante) ON DELETE CASCADE,
    CONSTRAINT fk_ed_direccion FOREIGN KEY (id_direccion)
        REFERENCES Direccion(id_direccion) ON DELETE RESTRICT
)