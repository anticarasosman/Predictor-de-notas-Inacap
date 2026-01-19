-- Seed data para Pagos
-- Basado en datos de morosos

INSERT INTO Pagos (id_matricula, numero_documento, concepto, monto_total, monto_pagado, fecha_vencimiento, estado_pago, metodo_pago) VALUES
-- Camila Manríquez - Deuda
(1, 'DOC-2025-001', 'MATRICULA', 46166.00, 0.00, '2025-04-01', 'VENCIDO', 'TRANSFERENCIA_BANCARIA'),
(1, 'DOC-2025-002', 'ARANCEL', 511200.00, 0.00, '2025-05-01', 'VENCIDO', 'TRANSFERENCIA_BANCARIA'),

-- Tammy Adriazola - Deuda
(2, 'DOC-2025-003', 'MATRICULA', 46166.00, 0.00, '2025-04-01', 'VENCIDO', 'TRANSFERENCIA_BANCARIA'),

-- Anahí (sin deuda)
(4, 'DOC-2025-007', 'MATRICULA', 46166.00, 46166.00, '2025-04-01', 'PAGADO', 'WEBPAY');
