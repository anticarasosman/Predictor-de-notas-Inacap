CREATE_TABLE Pagos (
    id_pagos INT PRIMARY KEY AUTO_INCREMENT,
    
    id_matricula INT NOT NULL,
    FOREIGN KEY (id_matricula) REFERENCES Matricula(id_matricula) ON DELETE CASCADE,

    numero_documento VARCHAR(50) NOT NULL UNIQUE,
    concepto ENUM("MATRICULA", "ARANCEL", "CERTIFICADO", "PASE ESCOLAR", "INSCRIPCION DE PRACTICA") NOT NULL,
    monto_total DECIMAL(10,2) NOT NULL,
    monto_pagado DECIMAL(10,2) NOT NULL,
    saldo_pendiente DECIMAL(10,2) NOT NULL GENERATED ALWAYS AS (monto_total - monto_pagado) STORED,
    fecha_vencimiento DATE NOT NULL,
    fecha_pago DATE,
    estado_pago ENUM("PENDIENTE", "PAGADO", "VENCIDO", "EN MORA", "CONDONADO") NOT NULL,
    metodo_pago ENUM("EFECTIVO", "TARJETA_CREDITO", "TARJETA_DEBITO", "TRANSFERENCIA_BANCARIA", "WEBPAY") NOT NULL,
    obeservaciones TEXT,
    fecha_registro_pago DATE,

    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
)