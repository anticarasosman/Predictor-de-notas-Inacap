-- ============================================================================
-- Script para crear usuarios MySQL con permisos especificos
-- EJECUTAR COMO: mysql -u root -p < create_app_users.sql
-- ============================================================================

-- Usar base de datos mysql para gestionar usuarios
USE mysql;

-- ============================================================================
-- 1. USUARIO PARA LA APLICACION (sin contraseña, solo localhost)
-- ============================================================================
-- Permisos: SELECT, INSERT, UPDATE, DELETE en inacap_test
-- Sin contraseña (seguro porque solo funciona desde localhost)

DROP USER IF EXISTS 'inacap_app'@'localhost';
CREATE USER 'inacap_app'@'%' IDENTIFIED BY 'contraseña_segura';

GRANT SELECT, INSERT, UPDATE, DELETE 
  ON inacap_test.* 
  TO 'inacap_app'@'localhost';

FLUSH PRIVILEGES;


-- ============================================================================
-- 2. USUARIO PARA TESTING (sin contraseña, solo localhost)
-- ============================================================================
-- Permisos: TODOS en inacap_test (para que los tests puedan crear/eliminar)
-- Sin contraseña (seguro porque solo funciona desde localhost)

DROP USER IF EXISTS 'inacap_test'@'localhost';
CREATE USER 'inacap_test'@'localhost' IDENTIFIED BY '';

GRANT ALL PRIVILEGES 
  ON inacap_test.* 
  TO 'inacap_test'@'localhost';

FLUSH PRIVILEGES;


-- ============================================================================
-- 3. USUARIO PARA ADMIN/MANTENIMIENTO (con contraseña)
-- ============================================================================
-- Permisos: TODOS en todas las bases de datos
-- Con contraseña fuerte (solo para desarrollo/mantenimiento)

DROP USER IF EXISTS 'inacap_admin'@'localhost';
CREATE USER 'inacap_admin'@'localhost' IDENTIFIED BY 'Admin_Temporal_123';

GRANT ALL PRIVILEGES 
  ON *.* 
  TO 'inacap_admin'@'localhost' WITH GRANT OPTION;

FLUSH PRIVILEGES;


-- ============================================================================
-- Verificacion: Mostrar los usuarios creados
-- ============================================================================

SELECT USER FROM mysql.user WHERE USER LIKE 'inacap%';

-- ============================================================================
-- INFORMACION IMPORTANTE:
-- ============================================================================
--
-- Usuario: inacap_app
--   - Contraseña: (ninguna)
--   - Permisos: SELECT, INSERT, UPDATE, DELETE
--   - Uso: Aplicación principal de INACAP
--   - Conexion: mysql -u inacap_app -h localhost
--
-- Usuario: inacap_test
--   - Contraseña: (ninguna)
--   - Permisos: TODOS (CREATE, DROP, ALTER, etc.)
--   - Uso: Automatización de tests con pytest
--   - Conexion: mysql -u inacap_test -h localhost
--
-- Usuario: inacap_admin
--   - Contraseña: Admin_Temporal_123
--   - Permisos: TODOS en todas las bases de datos
--   - Uso: Mantenimiento y administration
--   - Conexion: mysql -u inacap_admin -p -h localhost
--
-- CAMBIAR CONTRASEÑA DE ADMIN (recomendado):
--   ALTER USER 'inacap_admin'@'localhost' IDENTIFIED BY 'tu_nueva_contraseña_fuerte';
--
-- ============================================================================
