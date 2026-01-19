-- Seed data para Transaccion_Pago
-- Transacciones de pago realizadas

INSERT INTO Transaccion_Pago (id_cuota, id_estudiante, id_pago, monto_transaccion, tipo_transaccion, metodo_pago, numero_comprobante, fecha_transaccion, usuario_registro) VALUES
(1, 4, 4, 46166.00, 'PAGO', 'WEBPAY', 100001, '2025-03-20 10:30:00', 'Sistema WebPay');
