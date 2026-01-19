CREATE_TABLE Cuota (
    id_cuota INT PRIMARY KEY AUTO_INCREMENT,
    
    id_plan_estudio INT NOT NULL,
    FOREIGN KEY (id_plan_estudio) REFERENCES Planes_Estudio(id_plan_estudio) ON DELETE CASCADE,

    numero_cuota INT NOT NULL,
    /* Formato es: cuota X de X (Ej: cuota 3 de 5)*/
    total_cuotas VARCHAR(20) NOT NULL, 
    monto_cuota DECIMAL(10,2) NOT NULL,
    monto_pagado DECIMAL(10,2) DEFAULT 0.00,
    saldo_pendiente DECIMAL(10,2) NOT NULL GENERATED ALWAYS AS (monto_cuota - monto_pagado) STORED,
    fecha_vencimiento DATE NOT NULL,
    fecha_pago DATE,
    estado_cuota ENUM("PENDIENTE", "PAGADO", "VENCIDO", "EN MORA", "CONDONADO", "ATRASADA") NOT NULL,
    dias_mora INT DEFAULT 0,
    interes_mora DECIMAL(10,2) DEFAULT 0.00,

    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP

    UNIQUE (id_plan_estudio, numero_cuota)
)