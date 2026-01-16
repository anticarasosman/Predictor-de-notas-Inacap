@echo off
REM Script para instalar dependencias y ejecutar tests en Windows

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║           SETUP TESTING - Base de Datos INACAP                ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ✗ Python no está instalado o no está en el PATH
    echo   Descárgalo desde: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✓ Python detectado
echo.

REM Instalar dependencias
echo Instalando dependencias...
echo.
pip install -r requirements-testing.txt

if errorlevel 1 (
    echo ✗ Error al instalar dependencias
    pause
    exit /b 1
)

echo.
echo ✓ Dependencias instaladas correctamente
echo.

REM Menu de opciones
:menu
echo ════════════════════════════════════════════════════════════════
echo SELECCIONA UNA OPCION:
echo ════════════════════════════════════════════════════════════════
echo.
echo 1. Ejecutar TODOS los tests
echo 2. Ejecutar solo tests de DATOS VALIDOS
echo 3. Ejecutar solo tests de DATOS INVALIDOS
echo 4. Ejecutar solo tests de CASCADE/RESTRICT
echo 5. Ver EJEMPLOS PRACTICOS
echo 6. Ejecutar tests con output DETALLADO (con -s flag)
echo 7. Salir
echo.
set /p choice="Ingresa tu opción (1-7): "

if "%choice%"=="1" (
    echo.
    echo Ejecutando TODOS los tests...
    pytest test_database.py -v
    pause
    goto menu
)

if "%choice%"=="2" (
    echo.
    echo Ejecutando tests de DATOS VALIDOS...
    pytest test_database.py::TestInsertarDatosValidos -v
    pause
    goto menu
)

if "%choice%"=="3" (
    echo.
    echo Ejecutando tests de DATOS INVALIDOS...
    pytest test_database.py::TestInsertarDatosInvalidos -v
    pause
    goto menu
)

if "%choice%"=="4" (
    echo.
    echo Ejecutando tests de CASCADE/RESTRICT...
    pytest test_database.py::TestConstraintsCascadeRestrict -v
    pause
    goto menu
)

if "%choice%"=="5" (
    echo.
    echo Ejecutando EJEMPLOS PRACTICOS...
    python ejemplos_testing.py
    pause
    goto menu
)

if "%choice%"=="6" (
    echo.
    echo Ejecutando todos los tests con output DETALLADO...
    pytest test_database.py -v -s
    pause
    goto menu
)

if "%choice%"=="7" (
    echo.
    echo ¡Hasta luego!
    exit /b 0
)

echo.
echo ✗ Opción no válida
goto menu
