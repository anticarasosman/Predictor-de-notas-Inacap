@echo off
REM setup_db.bat
REM Script para ejecutar setup de la base de datos sin pedir contraseña cada vez
REM REQUISITO: Haber ejecutado previamente:
REM   mysql_config_editor.exe set --login-path=local --host=localhost --user=root --password

echo.
echo ================================
echo Iniciando setup de base de datos
echo ================================
echo.

REM Navegar a carpeta MySQL
cd /d "C:\Program Files\MySQL\MySQL Server 8.0\bin"

REM Ejecutar setup usando credenciales guardadas en mylogin.cnf
mysql.exe --login-path=local < "C:\Users\gstaudt\Desktop\Predictor-de-notas-Inacap\database\set_up.sql"

REM Mostrar resultado
if %errorlevel% equ 0 (
    echo.
    echo ===================================
    echo [OK] Base de datos creada exitosamente!
    echo ===================================
) else (
    echo.
    echo ===================================
    echo [ERROR] Hubo un problema
    echo ===================================
)

echo.
pause
