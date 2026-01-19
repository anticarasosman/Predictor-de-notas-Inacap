CREATE_TABLE Ramos_Plan_Estudio(
    id_ramo_plan_estudio INT PRIMARY KEY AUTO_INCREMENT,

    /* En que semestre esta el plan */
    semestre_plan INT NOT NULL,
    tipo_asignatura ENUM('OBLIGATORIA', 'OPTATIVA', 'LIBRE ELECCION') NOT NULL,
    orden_malla INT NOT NULL,
    /* JSON con ID's de ramos que requieren este */
    es_prerequisito_de TEXT,
    activo_en_plan BOOLEAN DEFAULT TRUE
)    