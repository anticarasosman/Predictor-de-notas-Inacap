CREATE_TABLE Ramos_Plan_Estudio_Prequsito(
    id_ramo_plan_estudio_prerequisito INT PRIMARY KEY AUTO_INCREMENT,

    id_ramo_plan_estudio INT NOT NULL,
    FOREIGN KEY (id_ramo_plan_estudio) REFERENCES Ramos_Plan_Estudio(id_ramo_plan_estudio) ON DELETE CASCADE,

    id_prerequisito INT NOT NULL,
    FOREIGN KEY (id_prerequisito) REFERENCES Prerequisitos(id_prerequisito) ON DELETE CASCADE
)