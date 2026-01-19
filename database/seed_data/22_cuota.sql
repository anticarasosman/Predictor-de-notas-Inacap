-- Seed data para Cuota
-- Cuotas de pagos

INSERT INTO Cuota (id_pago, numero_cuota, total_cuotas, monto_cuota, monto_pagado, fecha_vencimiento, estado_cuota, dias_mora) VALUES
-- Cuotas del arancel de Camila
(2, 1, 'cuota 1 de 10', 51120.00, 0.00, '2025-04-01', 'VENCIDO', 30),
(2, 2, 'cuota 2 de 10', 51120.00, 0.00, '2025-05-01', 'VENCIDO', 0),
(2, 3, 'cuota 3 de 10', 51120.00, 0.00, '2025-06-01', 'PENDIENTE', 0);
