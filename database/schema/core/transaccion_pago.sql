CREATE TABLE Transaccion_Pago (
    id_transaccion_pago INT PRIMARY KEY AUTO_INCREMENT,
    
    id_cuota INT NOT NULL,
    SECONDARY KEY (id_cuota) REFERENCES Cuota(id_cuota) ON DELETE CASCADE,
    id_estudiante INT NOT NULL,
    SECONDARY KEY (id_estudiante) REFERENCES Estudiante(id_estudiante) ON DELETE CASCADE,
    id_pagos INT NOT NULL,
    SECONDARY KEY (id_pagos) REFERENCES Pagos(id_pagos) ON DELETE CASCADE,

    monto_transaccion DECIMAL(10,2) NOT NULL,
    tipo_transaccion ENUM("PAGO", "AJUSTE", "CONDONACION", "DEVOLUCION") NOT NULL,
    metodo_pago ENUM("EFECTIVO", "TARJETA_CREDITO", "TARJETA_DEBITO", "TRANSFERENCIA_BANCARIA", "PAYPAL") NOT NULL,
    numero_comprobante INT NOT NULL,
    fecha_transaccion TIMESTAMP,
    /* Nombre de quien registro el pago */
    usuario_registro VARCHAR(100) NOT NULL,
    obeservaciones TEXT,

    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
)