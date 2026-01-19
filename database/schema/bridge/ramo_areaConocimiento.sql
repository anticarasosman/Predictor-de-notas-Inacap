CREATE_TABLE Ramo_AreaConocimiento (
    id_ramo INT NOT NULL,
    id_area_conocimiento INT NOT NULL,

    PRIMARY KEY (id_ramo, id_area_conocimiento),

    CONSTRAINT fk_ra_ac_ramo FOREIGN KEY (id_ramo)
        REFERENCES Ramo(id_ramo) ON DELETE CASCADE,
    CONSTRAINT fk_ra_ac_area_conocimiento FOREIGN KEY (id_area_conocimiento)
        REFERENCES Area_Conocimiento(id_area_conocimiento) ON DELETE CASCADE
)