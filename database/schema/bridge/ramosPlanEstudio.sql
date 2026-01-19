CREATE TABLE Ramos_Plan_Estudio_Ramo(
    id_ramos_plan_estudio_ramo INT PRIMARY KEY AUTO_INCREMENT,

    id_ramo_plan_estudio INT NOT NULL,
    FOREIGN KEY (id_ramo_plan_estudio) REFERENCES Ramos_Plan_Estudio(id_ramo_plan_estudio) ON DELETE CASCADE,

    id_ramo INT NOT NULL,
    FOREIGN KEY (id_ramo) REFERENCES Ramo(id_ramo) ON DELETE CASCADE
)