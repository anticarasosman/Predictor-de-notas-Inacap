-- ============================================================================
-- INICIALIZACIÓN DE TRIGGERS
-- ============================================================================
-- Este archivo carga todos los triggers de la base de datos en orden
-- de dependencia lógica
-- ============================================================================

-- ============================================================================
-- 1. CORE TRIGGERS (Timestamps y validaciones básicas)
-- ============================================================================
SOURCE database/triggers/01_core/timestamps.sql;

-- ============================================================================
-- 2. ACADEMIC TRIGGERS
-- ============================================================================
-- SOURCE database/triggers/02_academic/notas_estudiante.sql;
-- SOURCE database/triggers/02_academic/inscripciones_ramos.sql;
-- SOURCE database/triggers/02_academic/matricula.sql;
-- SOURCE database/triggers/02_academic/ramos_plan_estudio.sql;

-- ============================================================================
-- 3. FINANCIAL TRIGGERS
-- ============================================================================
-- SOURCE database/triggers/03_financial/pago.sql;
-- SOURCE database/triggers/03_financial/cuota.sql;
-- SOURCE database/triggers/03_financial/transaccion_pago.sql;

-- ============================================================================
-- 4. SECTIONS TRIGGERS
-- ============================================================================
-- SOURCE database/triggers/04_sections/secciones_ramos.sql;

-- ============================================================================
-- 5. VALIDATION TRIGGERS
-- ============================================================================
-- SOURCE database/triggers/05_validation/estudiante_colegio.sql;
-- SOURCE database/triggers/05_validation/estudiante_direccion.sql;
-- SOURCE database/triggers/05_validation/prerequisitos.sql;

-- ============================================================================
-- 6. PREDICTOR TRIGGERS
-- ============================================================================
-- SOURCE database/triggers/06_predictor/predictor_datos.sql;
